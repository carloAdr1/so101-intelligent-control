# Teleoperation Test

## Port configuration

- `/dev/ttyACM0` = follower / robot
- `/dev/ttyACM1` = leader / controller

## Set permissions

```bash
sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyACM1
```

## Run teleoperation

```bash
lerobot-teleoperate \
  --fps=25 \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM1
```
