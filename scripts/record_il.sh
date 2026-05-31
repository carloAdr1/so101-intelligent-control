#!/bin/bash
# Usage: bash scripts/record_il.sh <situation> <num_episodes>
# Situations: both_bw | only_black | only_white
SITUATION=${1:-both_bw}
NUM_EPISODES=${2:-100}
sudo chmod 666 /dev/video0 /dev/video2
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.cameras='{"front":{"type":"opencv","index_or_path":0,"width":640,"height":480,"fps":30},"side":{"type":"opencv","index_or_path":2,"width":640,"height":480,"fps":30}}' \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM1 \
  --dataset.repo_id=caadmi/cables_il_${SITUATION} \
  --dataset.root=./data/cables_il_${SITUATION} \
  --dataset.single_task="state based cable sorting: red yellow green targets, black white distractors" \
  --dataset.num_episodes=${NUM_EPISODES} \
  --dataset.episode_time_s=40 \
  --dataset.reset_time_s=5 \
  --dataset.fps=30 \
  --dataset.push_to_hub=false \
  --play_sounds=false
