#!/bin/bash
# Run full calibration for SO-101 follower and leader arms.
# Saves calibration files to ~/.cache/huggingface/lerobot/calibration/
# After calibration, copy files back with: bash scripts/load_calibration.sh

echo "Calibrating SO-101 follower (ttyACM0)..."
lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0

echo "Calibrating SO-101 leader (ttyACM1)..."
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM1

echo "Calibration complete."
echo "To save calibration to repo: copy from ~/.cache/huggingface/lerobot/calibration/"
