#!/bin/bash
# Usage: bash scripts/record_vla.sh <color> <num_episodes>
# Colors: red | yellow | green | black | white
COLOR=${1:-red}
NUM_EPISODES=${2:-100}
sudo chmod 666 /dev/video0 /dev/video2
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.cameras='{"front":{"type":"opencv","index_or_path":0,"width":640,"height":480,"fps":30},"side":{"type":"opencv","index_or_path":2,"width":640,"height":480,"fps":30}}' \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM1 \
  --dataset.repo_id=caadmi/cables_vla_${COLOR} \
  --dataset.root=./data/cables_vla_${COLOR} \
  --dataset.single_task="remove the ${COLOR} cable and place it in the ${COLOR} box" \
  --dataset.num_episodes=${NUM_EPISODES} \
  --dataset.episode_time_s=40 \
  --dataset.reset_time_s=5 \
  --dataset.fps=30 \
  --dataset.push_to_hub=false \
  --play_sounds=false
