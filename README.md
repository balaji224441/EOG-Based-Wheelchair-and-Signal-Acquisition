# 👁️ EOG-Based Wheelchair and Signal Acquisition

## Eye-Movement Controlled Assistive Mobility and Biomedical EOG Signal Acquisition System

An integrated biomedical engineering project combining **Electrooculography (EOG) signal acquisition, eye-movement recognition, embedded systems, Python-based signal recording, dataset generation, and EOG-based wheelchair control**.

The project consists of three major components:

1. **EOG-Based Wheelchair Prototype**
2. **EOG Signal Acquisition System**
3. **EOG Signal Dataset Collection**

The EOG acquisition system records horizontal and vertical eye-movement signals using an ESP32. The acquired signals are recorded and organized into a labeled dataset. The wheelchair prototype demonstrates how EOG-based eye movements can be mapped to directional wheelchair commands.

---

# 📌 Project Overview

Electrooculography (EOG) is a biomedical signal acquisition technique used to detect eye movements by measuring electrical potential variations associated with changes in eye position.

This project explores EOG signals as a human-machine interface for assistive mobility applications.

The complete project combines:

- Biomedical signal acquisition
- Embedded systems
- ESP32
- Arduino-based wheelchair control
- EOG signal recording
- Python programming
- Serial communication
- Signal visualization
- Dataset generation
- Eye-movement command mapping
- Assistive technology

The overall concept is:

```text
                    EOG SYSTEM
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
 EOG Signal Acquisition       EOG Wheelchair Control
          │                           │
          ▼                           ▼
 ESP32 + EOG Electrodes       Eye-Movement Commands
          │                           │
          ▼                           ▼
 Python Recording             Signal Processing
          │                           │
          ▼                           ▼
 CSV + Signal Plots           Direction Classification
          │                           │
          ▼                           ▼
      EOG Dataset             Wheelchair Movement
