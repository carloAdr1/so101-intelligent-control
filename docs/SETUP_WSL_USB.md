# Setup WSL + USBIPD

## 1. PowerShell (as administrator)

List devices:
```powershell
usbipd list
```

Share and attach cameras/arms:
```powershell
usbipd bind --busid <BUSID>
usbipd attach --wsl --busid <BUSID>
```

Example for this project:
```powershell
usbipd attach --wsl --busid 1-1
usbipd attach --wsl --busid 2-2
```

## 2. In Ubuntu/WSL

```bash
cd ~/so101_project
source venv/bin/activate
ls /dev/video*
ls /dev/ttyACM*

sudo chmod 666 /dev/video0 /dev/video2
sudo chmod 666 /dev/ttyACM0 /dev/ttyACM1
```
