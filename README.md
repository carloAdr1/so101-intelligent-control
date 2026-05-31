# SO101 Intelligent Control — Final Project

## Tracks
- **IL (Imitation Learning):** Carlos — caadmi
- **VLA:** [nombres amigos]

## Task
Option 2: Laboratory Setup with Clip Wires — SO101 sorts colored cables into matching boxes based on scene state.

## Hardware Setup

### Windows PowerShell (admin) — run every session
    usbipd attach --wsl --busid 1-1
    usbipd attach --wsl --busid 2-2

### WSL
    source venv/bin/activate
    bash scripts/setup_cameras.sh

### Robot ports
- /dev/ttyACM0 = SO101 follower (robot)
- /dev/ttyACM1 = SO101 leader (teleop)

## Installation
    git clone https://github.com/carloAdr1/so101-intelligent-control.git
    cd so101-intelligent-control
    python -m venv venv
    source venv/bin/activate
    pip install lerobot

## Recording Demos

### IL Track (3 situations x 100 episodes)
    bash scripts/record_il.sh both_bw 100
    bash scripts/record_il.sh only_black 100
    bash scripts/record_il.sh only_white 100

### VLA Track (3 colors x 100 episodes)
    bash scripts/record_vla.sh red 100
    bash scripts/record_vla.sh yellow 100
    bash scripts/record_vla.sh green 100

## Dataset
Hosted on Hugging Face — links will be added after upload.

## Repository Structure
    so101-intelligent-control/
    scripts/
        setup_cameras.sh
        record_il.sh
        record_vla.sh
    src/
        preprocessing/
        perception/
        training/
        evaluation/
        robot_execution/
    results/
        metrics/
        plots/
        videos/
    .gitignore
    README.md
