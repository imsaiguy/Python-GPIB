import serial
import numpy as np
import matplotlib.pyplot as plt
import time

# Set parameters
start_current = 0.001 # starting current
current_step = 0.001
max_current = 0.020   # stop current
max_voltage = 20
soak_time = 0.01      # seconds

# Arrays to store data for plotting

current_values = []
voltage_values = []
# Open the serial port
ser = serial.Serial('COM3', baudrate=9600, timeout=1)  # open serial port
print('Port: ', ser.name)  # check which port was really used

# Set SMU parameters
if ser.is_open:
    ser.write(b'++mode 1\n')  # controller mode
    ser.write(b'++auto 0\n')  # auto read after write
    ser.write(b'++addr 24\n')
    ser.write(b'*IDN?\n')
    ser.write(b'++read eoi\n')
    s = ser.readline().decode().strip()
    if len(s) > 0:
        print('SMU: ', s)


ser.write(b'*RST\n')
ser.write(b':*CLS\n')
ser.write(b':SOUR:FUNC:MODE CURR\n')
ser.write(b':SENS:FUNC "VOLT"\n')
ser.write(f':SENS:VOLT:PROT:LEV {max_voltage}\n'.encode())
ser.write(b':OUTP ON\n')
# Loop through currents
for current_setpoint in np.arange(start_current, max_current + current_step, current_step):
    # Set the current
    ser.write(f':SOUR:CURR:LEV {current_setpoint}\n'.encode())
    ser.write(b':INIT\n')
    time.sleep(soak_time)  # Wait for stabilization
    # Measure voltage
    ser.write(b':READ?\n')
    ser.write(b'++read eoi\n')
    measurement = ser.readline().decode().strip()
    numbers = measurement.strip().split(',')
    num1, num2, num3, num4, num5 = map(float, numbers)  # Use float() if numbers can have decimals

    print(f"Current: {num2}", end='')
    print(f" Voltage: {num1}")
    # Store data for plotting
    current_values.append(num2*1000)  # Convert to mA
    voltage_values.append(num1)

# Plot the data
plt.plot(voltage_values, current_values, marker='o', linestyle='-', color='b')
plt.ylabel('Current (mA)')
plt.xlabel('Voltage (V)')
plt.title('Current vs Voltage')
plt.grid(True)
plt.show()

# Clean up
ser.write(b':OUTP OFF\n')
ser.close()
