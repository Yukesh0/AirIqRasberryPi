# PMS5003 Sensor Setup Guide for Raspberry Pi

## Hardware Connections

| PMS5003 Pin | Wire Color | Raspberry Pi Pin | Description |
|-------------|------------|------------------|-------------|
| Pin 1 (VCC) | Red        | Pin 2 or 4 (5V)  | Power Supply |
| Pin 2 (GND) | Black      | Pin 6 (GND)      | Ground |
| Pin 4 (TXD) | Yellow     | Pin 10 (RXD/GPIO15) | Sensor TX to Pi RX |
| Pin 5 (RXD) | Green      | Pin 8 (TXD/GPIO14)  | Sensor RX to Pi TX |

**Note:** Pins 3 (SET) and 6 (RESET) can be left unconnected for basic operation.

## Raspberry Pi Configuration

### 1. Disable Serial Console (Required)

The Raspberry Pi uses the serial port for console access by default. You need to disable this:

```bash
# Open raspi-config
sudo raspi-config
```

Navigate to:
- **Interface Options** → **Serial Port**
- "Would you like a login shell accessible over serial?" → **No**
- "Would you like the serial port hardware to be enabled?" → **Yes**

Reboot your Raspberry Pi:
```bash
sudo reboot
```

### 2. Install Required Python Libraries

```bash
# Update package list
sudo apt-get update

# Install pip if not already installed
sudo apt-get install python3-pip

# Install pyserial library
pip3 install pyserial
```

### 3. Check Serial Port

Verify the serial port is available:
```bash
ls -l /dev/ttyS0
```

You should see something like:
```
crw-rw---- 1 root dialout 4, 64 Nov 26 10:00 /dev/ttyS0
```

### 4. Add User to dialout Group

To access the serial port without sudo:
```bash
sudo usermod -a -G dialout $USER
```

Log out and log back in for this to take effect.

## Running the Script

### Basic Usage

```bash
# Make the script executable
chmod +x pms5003_reader.py

# Run the script
python3 pms5003_reader.py
```

### Using the PMS5003 Class in Your Code

```python
from pms5003_reader import PMS5003

# Create sensor instance
sensor = PMS5003(port='/dev/ttyS0', baudrate=9600)

# Connect to sensor
if sensor.connect():
    # Read single measurement
    data = sensor.read_data()
    if data:
        print(f"PM2.5: {data['pm25_atm']} µg/m³")
    
    # Disconnect when done
    sensor.disconnect()
```

## Troubleshooting

### "Permission denied" error
- Make sure you added your user to the `dialout` group
- Log out and log back in
- Or run with `sudo` (not recommended)

### "Serial port not found"
- Check if `/dev/ttyS0` exists
- On some Raspberry Pi models, it might be `/dev/ttyAMA0`
- Verify hardware UART is enabled in raspi-config

### No data or timeout
- Check all wire connections
- Verify the sensor has power (5V)
- Make sure TX/RX are not swapped
- Wait 30 seconds after powering on for sensor to stabilize

### Checksum errors
- Check for loose connections
- Try a shorter cable
- Verify baudrate is 9600

## Understanding the Data

The sensor provides different PM concentration values:

- **PM1.0**: Particles with diameter < 1.0 µm
- **PM2.5**: Particles with diameter < 2.5 µm (most commonly reported)
- **PM10**: Particles with diameter < 10 µm

### Air Quality Index Reference

| PM2.5 (µg/m³) | Air Quality |
|---------------|-------------|
| 0-12          | Good        |
| 13-35         | Moderate    |
| 36-55         | Unhealthy for Sensitive Groups |
| 56-150        | Unhealthy   |
| 151-250       | Very Unhealthy |
| 251+          | Hazardous   |

## Additional Resources

- PMS5003 Datasheet: https://www.aqmd.gov/docs/default-source/aq-spec/resources-page/plantower-pms5003-manual_v2-3.pdf
- Raspberry Pi GPIO Pinout: https://pinout.xyz/
