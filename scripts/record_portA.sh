#!/bin/bash
# Port config A: follower=ttyACM0, leader=ttyACM1
SITUATION=${1:-only_black}
NUM_EPISODES=${2:-100}
sudo chmod 666 /dev/video0 /dev/video2
lerobot-record \
  --resume=true \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.cameras='{"front":{"type":"opencv","index_or_path":0,"width":640,"height":480,"fps":30},"side":{"type":"opencv","index_or_path":2,"width":640,"height":480,"fps":30}}' \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM1 \
  --dataset.repo_id=AdrielP/cables_il_${SITUATION} \
  --dataset.root=./data/cables_il_${SITUATION} \
  --dataset.single_task="state based cable sorting: red yellow green targets, black white distractors" \
  --dataset.num_episodes=${NUM_EPISODES} \
  --dataset.episode_time_s=30 \
  --dataset.reset_time_s=15 \
  --dataset.fps=30 \
  --dataset.push_to_hub=true \
  --play_sounds=false
