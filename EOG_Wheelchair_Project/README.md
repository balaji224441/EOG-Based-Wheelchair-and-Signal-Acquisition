# EOG-Based Wheelchair Control

### Eye-Movement Controlled Assistive Mobility Prototype

An Electrooculography (EOG)-based assistive wheelchair prototype that uses intentional eye movements to generate directional movement commands. The system acquires horizontal and vertical EOG signals, processes the signals to identify stable eye-movement patterns, and converts the detected commands into movement of a differential-drive wheelchair prototype.

---

## Project Overview

Electrooculography (EOG) is a biomedical signal acquisition technique that measures the electrical potential changes associated with eye movement.

This project explores the use of EOG signals as a human-machine interface for assistive mobility.

The developed prototype uses horizontal and vertical EOG information to distinguish intentional eye movements and map them to four directional commands:

- Forward
- Backward
- Left
- Right

The commands are processed by an Arduino-based control system and used to drive a differential-drive motor platform representing the wheelchair.

The project focuses on developing a low-cost, non-manual control interface that can be further extended toward assistive mobility applications.

---

# Project Objectives

The main objectives of the project are:

1. Acquire horizontal and vertical EOG signals from electrodes placed around the eyes.
2. Establish an adaptive baseline for the user's resting eye position.
3. Reduce signal fluctuations using digital filtering.
4. Detect intentional eye movements using threshold-based signal processing.
5. Validate commands using recent signal history and stability checks.
6. Distinguish horizontal and vertical eye movements.
7. Convert detected eye movements into directional wheelchair commands.
8. Control a differential-drive motor prototype.
9. Provide visual and serial feedback during system operation.
10. Develop a foundation for future intelligent assistive mobility systems.

---

# System Architecture

```text
             EOG Electrodes
                    |
                    v
          EOG Signal Acquisition
                    |
          +---------+---------+
          |                   |
          v                   v
   Horizontal EOG       Vertical EOG
          |                   |
          +---------+---------+
                    |
                    v
        Adaptive Baseline Calibration
                    |
                    v
          Moving Average Filtering
                    |
                    v
          Threshold-Based Detection
                    |
                    v
          Stability / History Check
                    |
                    v
           Axis Dominance Check
                    |
                    v
          Directional Command
                    |
          +---------+---------+
          |         |         |
          v         v         v
       Motor     LED       Serial
      Control   Feedback   Monitor
          |
          v
   Differential-Drive
      Wheelchair
