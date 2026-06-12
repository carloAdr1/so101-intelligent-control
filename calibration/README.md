# Calibration Files

Calibration files for the SO-101 arm used in this project.

> **Important:** these files are specific to the physical arm used in this project.
> If you use a different arm, recalibrate with: `bash scripts/calibrate.sh`

## Load this calibration

Copy the files to the path expected by lerobot:

```bash
mkdir -p ~/.cache/huggingface/lerobot/calibration/robots/so_follower
mkdir -p ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader

cp calibration/robots/so_follower.json ~/.cache/huggingface/lerobot/calibration/robots/so_follower/None.json
cp calibration/teleoperators/so_leader.json ~/.cache/huggingface/lerobot/calibration/teleoperators/so_leader/None.json
```

Or simply run: `bash scripts/load_calibration.sh`
