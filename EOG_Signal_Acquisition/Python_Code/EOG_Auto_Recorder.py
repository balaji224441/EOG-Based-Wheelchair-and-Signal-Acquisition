# EOG Automatic Recorder - Corrected Multi-Direction Version
# ESP32 + 2 BioAmp EXG Pills
# COM6, 115200 baud
# H_EOG = GPIO34, V_EOG = GPIO35
#
# Output:
# One CSV + one PNG (containing BOTH H and V plots) for every event.

import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import queue
import csv
import time
from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# ========================= SETTINGS =========================
BASE_FOLDER = Path(r"C:\Users\ASUS\Downloads\eogsignals")
SERIAL_PORT = "COM6"
BAUD_RATE = 115200
SAMPLE_RATE = 256

# Each tuple = (event name, instruction, seconds, save?)
PROTOCOL = [
    ("GET_READY", "GET READY", 3, False),

    ("STRAIGHT", "Look STRAIGHT", 5, True),
    ("REST_01", "REST", 2, False),

    ("LEFT", "Look LEFT", 3, True),
    ("REST_02", "REST", 2, False),

    ("RIGHT", "Look RIGHT", 3, True),
    ("REST_03", "REST", 2, False),

    ("UP", "Look UP", 3, True),
    ("REST_04", "REST", 2, False),

    ("DOWN", "Look DOWN", 3, True),
    ("REST_05", "REST", 2, False),

    ("BLINK_NORMAL", "BLINK NORMALLY", 5, True),
    ("REST_06", "REST", 2, False),

    ("BLINK_5X", "BLINK 5 TIMES", 5, True),
    ("REST_07", "REST", 2, False),

    ("STRAIGHT_FINAL", "Look STRAIGHT", 5, True),
]


class EOGRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("EOG Automatic Data Collection")
        self.root.geometry("1150x800")
        self.root.minsize(950, 700)

        self.serial = None
        self.serial_thread = None
        self.running_serial = False

        self.data_queue = queue.Queue()

        self.experiment_running = False
        self.stop_requested = False

        self.protocol_index = 0
        self.current_event = None
        self.current_instruction = ""
        self.current_duration = 0
        self.current_save = False
        self.event_start_time = None

        self.event_samples_h = []
        self.event_samples_v = []

        self.live_h = []
        self.live_v = []
        self.live_max = 1000

        self.session_folder = None
        self.trial_folder = None
        self.trial_number = 1
        self.subject_id = "TEST"
        self.total_trials = 1

        self.sample_counter = 0

        self.build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.after(50, self.process_serial_queue)
        self.root.after(100, self.update_countdown)

        self.connect_serial()

    # ========================= UI =========================
    def build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="EOG AUTOMATIC DATA COLLECTION",
                  font=("Arial", 20, "bold")).pack(anchor="w")

        info = ttk.Frame(top)
        info.pack(fill="x", pady=8)

        ttk.Label(info, text="Subject ID:").grid(row=0, column=0, padx=5)
        self.subject_entry = ttk.Entry(info, width=15)
        self.subject_entry.insert(0, "TEST")
        self.subject_entry.grid(row=0, column=1, padx=5)

        ttk.Label(info, text="Trials:").grid(row=0, column=2, padx=5)
        self.trials_entry = ttk.Entry(info, width=8)
        self.trials_entry.insert(0, "1")
        self.trials_entry.grid(row=0, column=3, padx=5)

        ttk.Label(info, text=f"Port: {SERIAL_PORT}").grid(row=0, column=4, padx=12)
        ttk.Label(info, text=f"Baud: {BAUD_RATE}").grid(row=0, column=5, padx=12)
        ttk.Label(info, text=f"Sampling: {SAMPLE_RATE} Hz").grid(row=0, column=6, padx=12)

        buttons = ttk.Frame(self.root, padding=(10, 0))
        buttons.pack(fill="x")

        self.start_button = ttk.Button(
            buttons, text="START EXPERIMENT",
            command=self.start_experiment
        )
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(
            buttons, text="STOP",
            command=self.stop_experiment,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)

        ttk.Button(
            buttons, text="CLEAR LIVE GRAPH",
            command=self.clear_live
        ).pack(side="left", padx=5)

        self.status_label = ttk.Label(
            buttons, text="Connecting...",
            font=("Arial", 11, "bold")
        )
        self.status_label.pack(side="right", padx=10)

        # Main instruction area
        self.instruction_label = tk.Label(
            self.root,
            text="READY",
            font=("Arial", 30, "bold"),
            pady=8
        )
        self.instruction_label.pack(fill="x")

        self.countdown_label = tk.Label(
            self.root,
            text="--",
            font=("Arial", 28, "bold")
        )
        self.countdown_label.pack()

        self.event_label = tk.Label(
            self.root,
            text="No experiment running",
            font=("Arial", 13)
        )
        self.event_label.pack(pady=3)

        self.file_label = tk.Label(
            self.root,
            text="Files will be saved to: " + str(BASE_FOLDER),
            font=("Arial", 10),
            anchor="w"
        )
        self.file_label.pack(fill="x", padx=15)

        # Live graph
        self.figure = Figure(figsize=(10, 5.2), dpi=100)
        self.ax_h = self.figure.add_subplot(211)
        self.ax_v = self.figure.add_subplot(212)

        self.ax_h.set_title("Live Horizontal EOG")
        self.ax_h.set_ylabel("ADC")
        self.ax_h.grid(True)

        self.ax_v.set_title("Live Vertical EOG")
        self.ax_v.set_xlabel("Samples")
        self.ax_v.set_ylabel("ADC")
        self.ax_v.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=10, pady=5
        )

    # ========================= SERIAL =========================
    def connect_serial(self):
        try:
            self.serial = serial.Serial(
                SERIAL_PORT,
                BAUD_RATE,
                timeout=0.1
            )
            time.sleep(1)
            self.running_serial = True

            self.status_label.config(
                text=f"CONNECTED - {SERIAL_PORT}"
            )

            self.serial_thread = threading.Thread(
                target=self.serial_reader,
                daemon=True
            )
            self.serial_thread.start()

        except Exception as e:
            self.status_label.config(
                text=f"NOT CONNECTED - {SERIAL_PORT}"
            )
            messagebox.showerror(
                "Serial Connection Error",
                f"Could not open {SERIAL_PORT}.\n\n"
                f"Close Arduino Serial Monitor and make sure ESP32 is connected.\n\n"
                f"Error:\n{e}"
            )

    def serial_reader(self):
        while self.running_serial:
            try:
                if self.serial and self.serial.in_waiting:
                    line = self.serial.readline().decode(
                        errors="ignore"
                    ).strip()

                    if not line:
                        continue

                    parts = line.split(",")

                    if len(parts) >= 2:
                        try:
                            h = float(parts[0].strip())
                            v = float(parts[1].strip())
                            self.data_queue.put((h, v))
                        except ValueError:
                            pass
                else:
                    time.sleep(0.002)

            except Exception:
                time.sleep(0.01)

    # ========================= SERIAL DATA =========================
    def process_serial_queue(self):
        count = 0

        while True:
            try:
                h, v = self.data_queue.get_nowait()
            except queue.Empty:
                break

            self.sample_counter += 1

            # Keep live graph
            self.live_h.append(h)
            self.live_v.append(v)

            if len(self.live_h) > self.live_max:
                self.live_h = self.live_h[-self.live_max:]
                self.live_v = self.live_v[-self.live_max:]

            # IMPORTANT:
            # Only collect event data while an actual SAVE event is active.
            if self.experiment_running and self.current_event and self.current_save:
                self.event_samples_h.append(h)
                self.event_samples_v.append(v)

            count += 1

        if count:
            self.update_live_graph()

        self.root.after(50, self.process_serial_queue)

    def update_live_graph(self):
        self.ax_h.clear()
        self.ax_v.clear()

        self.ax_h.plot(self.live_h)
        self.ax_v.plot(self.live_v)

        self.ax_h.set_title("Live Horizontal EOG")
        self.ax_h.set_ylabel("ADC")
        self.ax_h.grid(True)

        self.ax_v.set_title("Live Vertical EOG")
        self.ax_v.set_xlabel("Samples")
        self.ax_v.set_ylabel("ADC")
        self.ax_v.grid(True)

        self.canvas.draw_idle()

    def clear_live(self):
        self.live_h.clear()
        self.live_v.clear()
        self.update_live_graph()

    # ========================= EXPERIMENT =========================
    def start_experiment(self):
        if self.experiment_running:
            return

        try:
            subject = self.subject_entry.get().strip()
            if not subject:
                subject = "TEST"

            trials = int(self.trials_entry.get())
            if trials < 1:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Trials must be a positive integer."
            )
            return

        if not self.running_serial:
            messagebox.showerror(
                "Serial Error",
                f"{SERIAL_PORT} is not connected."
            )
            return

        self.subject_id = subject.replace(" ", "_")
        self.total_trials = trials

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.session_folder = (
            BASE_FOLDER /
            "EOG_Dataset" /
            self.subject_id /
            f"Session_{timestamp}"
        )

        self.session_folder.mkdir(parents=True, exist_ok=True)

        self.experiment_running = True
        self.stop_requested = False
        self.trial_number = 1
        self.protocol_index = 0

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.subject_entry.config(state="disabled")
        self.trials_entry.config(state="disabled")

        self.start_next_event()

    def start_next_event(self):
        if self.stop_requested:
            self.finish_experiment()
            return

        # If protocol is finished, move to next trial
        if self.protocol_index >= len(PROTOCOL):
            if self.trial_number < self.total_trials:
                self.trial_number += 1
                self.protocol_index = 0
                self.start_next_event()
            else:
                self.finish_experiment()
            return

        name, instruction, duration, should_save = PROTOCOL[self.protocol_index]

        self.current_event = name
        self.current_instruction = instruction
        self.current_duration = duration
        self.current_save = should_save

        self.event_samples_h = []
        self.event_samples_v = []
        self.event_start_time = time.perf_counter()

        self.trial_folder = (
            self.session_folder /
            f"Trial_{self.trial_number:02d}"
        )
        self.trial_folder.mkdir(parents=True, exist_ok=True)

        self.instruction_label.config(text=instruction)
        self.countdown_label.config(text=f"{duration:.1f} s")

        self.event_label.config(
            text=(
                f"Trial {self.trial_number}/{self.total_trials}   |   "
                f"Step {self.protocol_index + 1}/{len(PROTOCOL)}   |   "
                f"{name}"
            )
        )

        if should_save:
            self.file_label.config(
                text=f"RECORDING: {name}  →  CSV + H/V PNG"
            )
        else:
            self.file_label.config(
                text=f"Preparation/Rest: {name}"
            )

        # Schedule event completion using Tk after.
        self.root.after(
            int(duration * 1000),
            self.finish_current_event
        )

    def finish_current_event(self):
        # Protect against stale callbacks after STOP
        if not self.experiment_running:
            return

        event_name = self.current_event
        should_save = self.current_save

        # Save ONLY this event.
        if should_save:
            self.save_event(event_name)

        # Move to next protocol event.
        self.protocol_index += 1

        # Tiny delay before next event so the UI visibly changes.
        self.root.after(100, self.start_next_event)

    # ========================= SAVE CSV + GRAPH =========================
    def save_event(self, event_name):
        if self.trial_folder is None:
            return

        h = list(self.event_samples_h)
        v = list(self.event_samples_v)

        # Use the shorter channel length so every CSV row has both values.
        n = min(len(h), len(v))

        h = h[:n]
        v = v[:n]

        if n == 0:
            return

        csv_path = (
            self.trial_folder /
            f"Trial_{self.trial_number:02d}_{event_name}.csv"
        )

        png_path = (
            self.trial_folder /
            f"Trial_{self.trial_number:02d}_{event_name}_EOG.png"
        )

        # ---------- CSV ----------
        with open(
            csv_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "Time_s",
                "Sample",
                "H_EOG_ADC",
                "V_EOG_ADC",
                "Event"
            ])

            for i in range(n):
                writer.writerow([
                    f"{i / SAMPLE_RATE:.6f}",
                    i,
                    h[i],
                    v[i],
                    event_name
                ])

        # ---------- Combined H + V graph ----------
        fig = Figure(figsize=(11, 7), dpi=120)

        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        t = [i / SAMPLE_RATE for i in range(n)]

        ax1.plot(t, h)
        ax1.set_title(
            f"Horizontal EOG - {event_name} "
            f"(Trial {self.trial_number})"
        )
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("ADC")
        ax1.grid(True)

        ax2.plot(t, v)
        ax2.set_title(
            f"Vertical EOG - {event_name} "
            f"(Trial {self.trial_number})"
        )
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("ADC")
        ax2.grid(True)

        fig.tight_layout()
        fig.savefig(png_path, dpi=150)
        plt.close(fig)

        self.file_label.config(
            text=f"SAVED: {csv_path.name}  +  {png_path.name}"
        )

    # ========================= COUNTDOWN =========================
    def update_countdown(self):
        if (
            self.experiment_running
            and self.event_start_time is not None
        ):
            elapsed = time.perf_counter() - self.event_start_time
            remaining = max(0, self.current_duration - elapsed)

            self.countdown_label.config(
                text=f"{remaining:.1f} s"
            )

        self.root.after(100, self.update_countdown)

    # ========================= STOP =========================
    def stop_experiment(self):
        if not self.experiment_running:
            return

        self.stop_requested = True
        self.experiment_running = False

        self.current_event = None
        self.current_save = False

        self.instruction_label.config(text="STOPPED")
        self.countdown_label.config(text="--")
        self.event_label.config(text="Experiment stopped")

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.subject_entry.config(state="normal")
        self.trials_entry.config(state="normal")

    def finish_experiment(self):
        self.experiment_running = False
        self.current_event = None
        self.current_save = False
        self.event_start_time = None

        self.instruction_label.config(text="EXPERIMENT COMPLETE")
        self.countdown_label.config(text="✓")
        self.event_label.config(
            text=f"Completed {self.total_trials} trial(s)"
        )
        self.file_label.config(
            text=f"All files saved in: {self.session_folder}"
        )

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.subject_entry.config(state="normal")
        self.trials_entry.config(state="normal")

        messagebox.showinfo(
            "Experiment Complete",
            "All directions/events have been recorded.\n\n"
            f"Files saved in:\n{self.session_folder}"
        )

    # ========================= CLOSE =========================
    def on_close(self):
        self.running_serial = False
        self.experiment_running = False

        try:
            if self.serial:
                self.serial.close()
        except Exception:
            pass

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EOGRecorder(root)
    root.mainloop()
