# 🦽 EOG-Based Wheelchair

## Eye-Movement Controlled Assistive Wheelchair Using EOG Signals

The EOG-Based Wheelchair is an assistive mobility prototype that converts eye movements into directional wheelchair commands using Electrooculography (EOG) signals.

The system uses horizontal and vertical EOG signals to detect the user's eye-movement direction. The acquired signals are processed using calibration, filtering, threshold detection, signal-history validation, and direction classification. The resulting command is then used to control the wheelchair motors.

---

## 📌 Project Overview

The EOG-Based Wheelchair combines biomedical signal processing, embedded systems, motor control, and human-machine interaction into a single assistive mobility prototype.

The system consists of:

- EOG electrodes for eye-movement signal acquisition
- Horizontal EOG signal for left/right movement detection
- Vertical EOG signal for up/down movement detection
- Signal calibration and baseline estimation
- Moving-average filtering
- Threshold-based movement detection
- Signal-history validation
- Axis-dominance checking
- Direction classification
- Arduino-based wheelchair control
- Motor driver for motor actuation
- Two-wheel differential drive
- Serial monitoring for command verification

The detected eye movements are mapped to four wheelchair directions:

- Forward
- Backward
- Left
- Right

---

## ✨ Features

- 👁️ Eye-movement-based wheelchair control
- 📈 Horizontal and vertical EOG signal processing
- ⚙️ Automatic baseline calibration
- 🔄 Moving-average signal filtering
- 🎯 Threshold-based command detection
- 🧠 Signal-history validation
- ↔️ Horizontal eye-movement detection
- ↕️ Vertical eye-movement detection
- 🦽 Four-direction wheelchair movement
- ⚡ Arduino-based real-time control
- 🔧 Differential motor control
- 💻 Serial command monitoring
- 🛡️ Ambiguous movement rejection
- ⏱️ Controlled movement execution
- 🤖 Biomedical human-machine interface

---

## 🔧 Hardware Used

| Component | Quantity | Purpose |
|---|---:|---|
| Arduino Uno | 1 | Main wheelchair controller |
| EOG Electrodes | 4+ | Eye-movement signal acquisition |
| EOG Signal Acquisition Circuit | 2 Channels | Horizontal and vertical EOG |
| Motor Driver | 1 | Motor control |
| DC Motors | 2 | Wheelchair movement |
| Wheelchair Prototype | 1 | Mobility platform |
| Battery / Power Supply | 1 | System power |
| Connecting Wires | - | Electrical connections |

---

## 🎯 Eye-Movement to Wheelchair Mapping

The detected eye movements are mapped to the corresponding wheelchair commands.

| Eye Movement | Wheelchair Command |
|---|---|
| Eyes Up | Forward |
| Eyes Down | Backward |
| Eyes Left | Left |
| Eyes Right | Right |

The basic directional mapping is:

```text
Eyes Up     → Forward
Eyes Down   → Backward
Eyes Left   → Left
Eyes Right  → Right
