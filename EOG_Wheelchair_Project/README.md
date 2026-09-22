# EOG-Based Wheelchair Control

## Eye-Movement Controlled Assistive Mobility Prototype

An Electrooculography (EOG)-based assistive mobility prototype that uses intentional eye movements to generate directional wheelchair commands. The system acquires horizontal and vertical EOG signals, performs signal conditioning and command validation, and converts recognized eye-movement intentions into movement commands for a differential-drive wheelchair prototype.

---

# Project Overview

Electrooculography (EOG) is a biomedical signal acquisition technique that measures electrical potential variations associated with eye movements.

This project explores EOG as a hands-free human-machine interface for assistive mobility.

The system uses two EOG signal channels:

- Horizontal EOG (H-EOG)
- Vertical EOG (V-EOG)

The acquired signals are processed to identify intentional eye movements. The recognized eye movement is then converted into a directional command for the wheelchair prototype.

The basic directional command set consists of:

- Forward
- Backward
- Left
- Right

The project combines:

- Biomedical signal acquisition
- EOG signal processing
- Digital filtering
- Threshold-based command recognition
- Embedded systems
- Motor control
- Differential-drive robotics
- Assistive technology

---

# Project Objective

The primary objective of this project is to develop a low-cost assistive mobility interface in which intentional eye movements can be used to control the direction of a wheelchair prototype.

The system is designed to:

1. Acquire horizontal and vertical EOG signals.
2. Establish a resting baseline for the user.
3. Remove baseline offset from the acquired signals.
4. Smooth the EOG signals using a moving-average filter.
5. Detect sufficiently strong EOG activity.
6. Confirm the persistence of the detected signal.
7. Verify temporal stability using recent signal history.
8. Determine whether the movement is primarily horizontal or vertical.
9. Identify the intended wheelchair direction.
10. Execute the corresponding motor command.
11. Prevent conflicting commands during movement.

---

# System Concept

The complete system can be represented as:

```text
              USER
                |
                |
          Eye Movements
                |
                v
        +---------------+
        | EOG Electrodes|
        +---------------+
                |
                v
       EOG Signal Acquisition
                |
        +-------+-------+
        |               |
        v               v
   Horizontal EOG   Vertical EOG
        |               |
        +-------+-------+
                |
                v
      Adaptive Baseline
          Calibration
                |
                v
      Moving Average Filter
                |
                v
       Threshold Evaluation
                |
                v
      Persistence Confirmation
                |
                v
       Stability Verification
                |
                v
       Axis Dominance Check
                |
                v
       Direction Recognition
                |
                v
       Wheelchair Command
                |
                v
       Motor Control System
                |
                v
      Differential-Drive
         Wheelchair
