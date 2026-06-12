# SO101 Calibration

## Follower

```bash
lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0
```

## Leader

```bash
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM1
```

If a calibration already exists, press ENTER to use it.
Use `c` only if you want to recalibrate from scratch.
