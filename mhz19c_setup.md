# MH-Z19C CO2 Sensor Setup Guide for Raspberry Pi

## Hardware Connections

The MH-Z19C has different pin configurations depending on the model. Most common pinout:

### Standard MH-Z19C (7-pin connector)

| MH-Z19C Pin | Function | Raspberry Pi Pin | GPIO/Description |
|-------------|----------|------------------|------------------|
| Vin         | Power    | Pin 2 or 4       | 5V (or 3.3V*)   |
| GND         | Ground   | Pin 6            | Ground           |
| RX (RXD)    | Receive  | Pin 8            | GPIO 14 (TXD)    |
| TX (TXD)    | Transmit | Pin 10           | GPIO 15 (RXD)    |
| HD          | -        | Not connected    | -                |
| PWM         | PWM Out  | Optional         | For PWM reading  |
| Vo          | Analog   | Not connected    | Not used         |

**Note:** Most MH-Z19C work with 3.3V-5V. Check your sensor datasheet.

### Important Wiring Notes
- Sensor TX connects to Pi RX (GPIO 15, Pin 10)
- Sensor RX connects to Pi TX (GPIO 14, Pin 8)
- If you also have the PMS5003 sensor, you **cannot use both simultaneously** on the same UART port

## Using Both Sensors (PMS5003 + MH-Z19C)

Since Raspberry Pi 4 has only one easily accessible UART (GPIO 14/15), you have three options:

### Option 1: Use USB-to-Serial Adapter (Recommended)
Connect one sensor to the hardware UART (/dev/ttyS0) and the other to a USB-to-serial adapter (/dev/ttyUSB0)

```python
# PMS5003 on hardware UART
pms_sensor = PMS5003(port='/dev/ttyS0')

# MH-Z19C on USB adapter
co2_sensor = MHZ19C(port='/dev/ttyUSB0')
```

### Option 2: Physical Switch
Manually switch the sensor connections when needed (not recommended for continuous monitoring)

### Option 3: Enable Secondary UART
Enable the mini UART on GPIO 0/1 (more complex, requires additional configuration)

## Raspberry Pi Configuration

If you've already set up the PMS5003 sensor, the UART is already configured. If not:

### 1. Disable Serial Console

```bash
sudo raspi-config
```
Navigate to: **Interface Options** → **Serial Port**
- Login shell: **No**
- Hardware enabled: **Yes**

### 2. Remove Serial Console from Boot

```bash
sudo cp /boot/firmware/cmdline.txt /boot/firmware/cmdline.txt.backup
sudo sed -i 's/console=serial0,115200 //' /boot/firmware/cmdline.txt
```

### 3. Enable UART

```bash
echo "enable_uart=1" | sudo tee -a /boot/firmware/config.txt
```

### 4. Reboot

```bash
sudo reboot
```

## Python Setup

pyserial is already installed if you set up the PMS5003. If not:

```bash
pip3 install pyserial
```

## Running the Script

### Basic Usage

```bash
python3 mhz19c_reader.py
```

### Using in Your Code

```python
from mhz19c_reader import MHZ19C

# Create sensor instance
sensor = MHZ19C(port='/dev/ttyS0', baudrate=9600)

# Connect
if sensor.connect():
    # Read single measurement
    data = sensor.read_co2()
    if data:
        print(f"CO2: {data['co2']} ppm")
        print(f"Temperature: {data['temperature']}°C")
    
    sensor.disconnect()
```

## Combined Sensor Reading Script

If using both sensors with USB adapter:

```python
from pms5003_reader import PMS5003
from mhz19c_reader import MHZ19C
import time

# PMS5003 on hardware UART
air_quality = PMS5003(port='/dev/ttyS0')

# MH-Z19C on USB adapter
co2_sensor = MHZ19C(port='/dev/ttyUSB0')

if air_quality.connect() and co2_sensor.connect():
    try:
        while True:
            # Read air quality
            aq_data = air_quality.read_data()
            if aq_data:
                print(f"PM2.5: {aq_data['pm25_atm']} µg/m³")
            
            # Read CO2
            co2_data = co2_sensor.read_co2()
            if co2_data:
                print(f"CO2: {co2_data['co2']} ppm")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopped")
    finally:
        air_quality.disconnect()
        co2_sensor.disconnect()
```

## Sensor Warm-up Time

**IMPORTANT:** The MH-Z19C requires:
- **3 minutes** minimum warm-up time for stable readings
- **24 hours** for most accurate readings after first power-on
- Do not read more frequently than every **5 seconds**

## Calibration

The MH-Z19C has automatic baseline calibration (ABC) that calibrates to 400ppm over 24 hours. 

### Manual Zero Point Calibration

Only if needed (sensor shows incorrect baseline):

1. Place sensor in fresh outdoor air (400ppm CO2)
2. Power on for 20+ minutes
3. Run calibration:

```python
sensor.calibrate_zero_point()
```

**WARNING:** Do not calibrate indoors! This will make readings inaccurate.

## Troubleshooting

### "Invalid response length" or "Checksum error"
- Check wiring connections
- Verify baudrate is 9600
- Wait for sensor warm-up (3+ minutes)

### No data received
- Verify TX/RX are not swapped
- Check power supply (3.3V-5V depending on model)
- Ensure serial console is disabled
- Try different serial port

### Very high or very low readings
- Sensor needs 24-hour warm-up for accuracy
- May need calibration in outdoor air
- Check if ABC (automatic baseline correction) is enabled

## CO2 Level Reference

| CO2 (ppm) | Air Quality         | Effects                          |
|-----------|---------------------|----------------------------------|
| 250-400   | Outdoor air         | Normal outdoor level             |
| 400-1000  | Good                | Acceptable indoor air quality    |
| 1000-2000 | Moderate            | Complaints, stuffiness           |
| 2000-5000 | Poor                | Drowsiness, poor air quality     |
| 5000+     | Very Poor           | Health effects, headaches        |

## Technical Specifications

- **Measurement Range:** 0-5000 ppm (0-10000 ppm optional)
- **Accuracy:** ±(50ppm + 5% of reading)
- **Response Time:** < 120 seconds
- **Warm-up Time:** 3 minutes (180 seconds)
- **Operating Voltage:** 3.6V - 5.5V (check your model)
- **Communication:** UART (9600 baud, 8N1)
