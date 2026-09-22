# 👁️ EOG Signal Acquisition System

## ESP32-Based Electrooculography Signal Recording and Dataset Collection

This project implements an ESP32-based Electrooculography (EOG) signal acquisition system for recording horizontal and vertical eye-movement signals.

The system acquires EOG signals from two channels, transfers the data through serial communication, and uses a Python-based recording application to display, organize, and save the signals.

The recorded signals are labeled according to different eye movements and blinking activities and are used to generate a structured EOG dataset.

---

## 📌 Project Overview

Electrooculography (EOG) is a biomedical signal technique used to measure eye movements by detecting the electrical potential changes associated with movement of the eyes.

In this project, two EOG signal channels are acquired:

- Horizontal EOG (H-EOG)
- Vertical EOG (V-EOG)

An ESP32 microcontroller is used for analog signal acquisition.

The acquired signals are transmitted through the serial interface to a Python application, where they are recorded and stored as CSV files along with corresponding signal plots.

---

## 🎯 Objectives

The main objectives of the project are:

- Acquire horizontal and vertical EOG signals.
- Use ESP32 for real-time analog signal acquisition.
- Sample the EOG signals at a fixed sampling frequency.
- Transmit acquired data through serial communication.
- Develop a Python-based EOG recording system.
- Record different eye-movement patterns.
- Record different blink patterns.
- Automatically save the acquired signals as CSV files.
- Generate signal plots for each recorded event.
- Organize the recordings into structured dataset sessions.
- Provide a dataset suitable for future EOG signal-processing and classification experiments.

---

## ⚙️ System Architecture

```text
                EOG Electrodes
                      │
                      ▼
             EOG Signal Acquisition
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
       Horizontal EOG      Vertical EOG
          H-EOG               V-EOG
             │                 │
             ▼                 ▼
          ESP32 ADC         ESP32 ADC
             │                 │
             └────────┬────────┘
                      │
                      ▼
              Serial Communication
                      │
                      ▼
               Python Recorder
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      CSV Dataset            Signal Plots
          │                       │
          └───────────┬───────────┘
                      ▼
                EOG Dataset
