#!/bin/bash
# Load calibration files from repo to lerobot cache
mkdir -p ~/.cache/huggingface/lerobot/calibration/robots/so_follower
mkdir -p ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader

cp calibration/robots/so_follower.json ~/.cache/huggingface/lerobot/calibration/robots/so_follower/None.json
cp calibration/teleoperators/so_leader.json ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/None.json

echo "Calibration loaded successfully"
