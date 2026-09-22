# EOG-Based Wheelchair Control

## Project Overview

This project presents an Electrooculography (EOG)-based wheelchair control system designed to enable directional movement using intentional eye movements.

The system acquires horizontal and vertical EOG signals from electrodes placed around the eyes. The signals are processed to identify stable gaze commands, which are then translated into directional movement of a differential-drive wheelchair prototype.

## Project Objective

The main objective is to develop a low-cost assistive mobility interface using EOG signals for directional control.

The prototype supports four discrete movement commands:

- Forward
- Backward
- Left
- Right

## System Architecture

```text
EOG Electrodes
      ↓
EOG Signal Acquisition
      ↓
Horizontal / Vertical EOG
      ↓
Adaptive Baseline Calibration
      ↓
Moving Average Filtering
      ↓
Command Validation
      ↓
Directional Command
      ↓
Motor Driver
      ↓
Differential-Drive Wheelchair
