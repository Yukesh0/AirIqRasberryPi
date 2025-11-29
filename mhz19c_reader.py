#!/usr/bin/env python3
"""
MH-Z19C CO2 Sensor Reader for Raspberry Pi
Reads CO2 concentration in ppm (parts per million)
"""

import serial
import time

class MHZ19C:
    """Class to read data from MH-Z19C CO2 sensor"""
    
    # Command to read CO2 concentration
    CMD_READ_CO2 = [0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
    
    def __init__(self, port='/dev/ttyS0', baudrate=9600, timeout=1):
        """
        Initialize MH-Z19C sensor
        
        Args:
            port: Serial port (default: /dev/ttyS0 for Raspberry Pi)
            baudrate: Communication speed (default: 9600)
            timeout: Read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        
    def connect(self):
        """Open serial connection to the sensor"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"Connected to MH-Z19C on {self.port}")
            time.sleep(2)  # Allow sensor to stabilize
            # Flush any existing data
            self.serial.flushInput()
            return True
        except serial.SerialException as e:
            print(f"Error connecting to sensor: {e}")
            return False
    
    def disconnect(self):
        """Close serial connection"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Disconnected from sensor")
    
    def _calculate_checksum(self, data):
        """Calculate checksum for MH-Z19C data"""
        checksum = 0xFF
        for byte in data[1:8]:
            checksum -= byte
        checksum += 1
        return checksum & 0xFF
    
    def read_co2(self):
        """
        Read CO2 concentration from sensor
        
        Returns:
            dict: Dictionary containing CO2 value and status or None if read fails
        """
        if not self.serial or not self.serial.is_open:
            print("Serial port not open")
            return None
        
        try:
            # Clear any pending data
            self.serial.flushInput()
            
            # Send read command
            self.serial.write(bytearray(self.CMD_READ_CO2))
            
            # Wait a bit for response
            time.sleep(0.1)
            
            # Read response (9 bytes)
            response = self.serial.read(9)
            
            if len(response) != 9:
                print(f"Invalid response length: {len(response)} bytes")
                return None
            
            # Verify start byte
            if response[0] != 0xFF:
                print(f"Invalid start byte: 0x{response[0]:02X}")
                return None
            
            # Verify command byte
            if response[1] != 0x86:
                print(f"Invalid command byte: 0x{response[1]:02X}")
                return None
            
            # Verify checksum
            checksum = self._calculate_checksum(response)
            if response[8] != checksum:
                print(f"Checksum error! Expected: 0x{checksum:02X}, Got: 0x{response[8]:02X}")
                return None
            
            # Extract CO2 concentration (bytes 2 and 3, high byte first)
            co2 = (response[2] << 8) | response[3]
            
            # Extract temperature (if available, byte 4 - 40)
            temp = response[4] - 40
            
            # Extract status (byte 5)
            status = response[5]
            
            return {
                'co2': co2,
                'temperature': temp,
                'status': status,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"Error reading data: {e}")
            return None
    
    def read_continuous(self, interval=5, duration=None):
        """
        Read CO2 data continuously from sensor
        
        Args:
            interval: Time between readings in seconds (minimum 5 seconds recommended)
            duration: Total duration to read in seconds (None = infinite)
        """
        if interval < 5:
            print("Warning: Reading interval less than 5 seconds may affect sensor accuracy")
        
        start_time = time.time()
        
        try:
            while True:
                data = self.read_co2()
                
                if data:
                    co2_level = self.get_co2_level(data['co2'])
                    print(f"\n[{data['timestamp']}]")
                    print(f"CO2:         {data['co2']} ppm")
                    print(f"Temperature: {data['temperature']}°C")
                    print(f"Level:       {co2_level}")
                else:
                    print("Failed to read data")
                
                time.sleep(interval)
                
                # Check if duration limit reached
                if duration and (time.time() - start_time) >= duration:
                    break
                    
        except KeyboardInterrupt:
            print("\n\nStopped by user")
    
    def get_co2_level(self, co2):
        """
        Get CO2 level description based on concentration
        
        Args:
            co2: CO2 concentration in ppm
            
        Returns:
            str: Description of CO2 level
        """
        if co2 < 400:
            return "Below normal (outdoor level)"
        elif co2 < 1000:
            return "Good (acceptable)"
        elif co2 < 2000:
            return "Moderate (some complaints)"
        elif co2 < 5000:
            return "Poor (drowsiness, stuffiness)"
        else:
            return "Very Poor (health effects)"
    
    def calibrate_zero_point(self):
        """
        Calibrate sensor zero point (400ppm)
        WARNING: Only use this in fresh outdoor air!
        Sensor should be powered on for at least 20 minutes before calibration
        """
        cmd = [0xFF, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78]
        
        response = input("Are you sure you want to calibrate? Sensor must be in 400ppm air (outdoor). Type 'YES' to confirm: ")
        if response != 'YES':
            print("Calibration cancelled")
            return False
        
        try:
            self.serial.write(bytearray(cmd))
            print("Zero point calibration command sent. Wait 20 seconds...")
            time.sleep(20)
            print("Calibration complete")
            return True
        except Exception as e:
            print(f"Calibration error: {e}")
            return False


def main():
    """Main function to demonstrate MH-Z19C usage"""
    
    # Create sensor instance
    sensor = MHZ19C(port='/dev/ttyS0', baudrate=9600)
    
    # Connect to sensor
    if not sensor.connect():
        print("Failed to connect to sensor. Check connections and serial port configuration.")
        return
    
    print("\nReading CO2 data...")
    print("Press Ctrl+C to stop\n")
    print("CO2 Level Reference:")
    print("  < 400 ppm:  Below normal (outdoor level)")
    print("  400-1000:   Good (acceptable indoor air)")
    print("  1000-2000:  Moderate (may cause complaints)")
    print("  2000-5000:  Poor (drowsiness, poor air)")
    print("  > 5000:     Very Poor (health effects)")
    print()
    
    try:
        # Read continuously every 5 seconds (sensor needs time between readings)
        sensor.read_continuous(interval=5)
    finally:
        # Ensure we disconnect properly
        sensor.disconnect()


if __name__ == "__main__":
    main()
