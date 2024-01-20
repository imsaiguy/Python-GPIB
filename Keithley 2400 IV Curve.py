# IMSAI Guy 2024
# control Keithley 2400 with Proglogix USB-GPIB interface
# force current, measure voltage, plot IV curve

import serial
import numpy as np
import matplotlib.pyplot as plt
import time

# Set parameters
start_current = 1   # (mA) starting current
current_step = 1    # (mA)
max_current = 20    # (mA) stop current
max_voltage = 10    # compliance voltage
soak_time = 0.01    # seconds

#convert to amps
start_current /= 1000   # amps
current_step  /= 1000   # amps
max_current   /= 1000   # amps
# Arrays to store data for plotting
current_values = []
voltage_values = []

# Open the serial port
ser = serial.Serial('COM3', baudrate=9600, timeout=1)  # open serial port
print('Port: ', ser.name)  # check which port was really used

# Set SMU parameters
ser.write(b'++mode 1\n')  # controller mode
ser.write(b'++auto 0\n')  # auto read after write
ser.write(b'++addr 24\n')
ser.write(b'*IDN?\n')
ser.write(b'++read eoi\n')
s = ser.readline().decode().strip()
print('SMU: ', s)

ser.write(b'*RST\n')    # reset
ser.write(b':*CLS\n')   # clear
ser.write(b':SOUR:FUNC:MODE CURR\n')  # force current
ser.write(b':SENS:FUNC "VOLT"\n')     # measure voltsage
ser.write(f':SENS:VOLT:PROT:LEV {max_voltage}\n'.encode())  # compliance
ser.write(b':OUTP ON\n')  # turn on output
# Loop through currents
for current_setpoint in np.arange(start_current, max_current + current_step, current_step):
    # Set the current
    ser.write(f':SOUR:CURR:LEV {current_setpoint}\n'.encode())  # set current level
    ser.write(b':INIT\n')  # do it
    time.sleep(soak_time)  # Wait for stabilization
    # Measure voltage
    ser.write(b':READ?\n')  # read data
    ser.write(b'++read eoi\n')
    measurement = ser.readline().decode().strip()
    numbers = measurement.strip().split(',')
    num1, num2, num3, num4, num5 = map(float, numbers)  # Use float() if numbers can have decimals
    # num1 = voltage
    # num2 = current
    # num3 = resistance
    # num4 = time
    # num5 = status
    print(f"Current: {num2}", end='')
    print(f" Voltage: {num1}")
    # Store data for plotting
    current_values.append(num2*1000)  # Convert to mA
    voltage_values.append(num1)
# Clean up
ser.write(b':OUTP OFF\n')  # turn off output
ser.close()

# Plot the data
plt.plot(voltage_values, current_values, marker='o', linestyle='-', color='b')
plt.ylabel('Current (mA)')
plt.xlabel('Voltage (V)')
plt.title('Current vs Voltage')
plt.grid(True)
plt.show()


