import serial

# Define the serial port settings
# Open the serial port
ser = serial.Serial('COM3',baudrate=9600,timeout=1)  # open serial port
print('Port: ',ser.name)         # check which port was really use
# need mode 1  - set to controller
#      auto 1  - read after write automatic
if ser.is_open:
    ser.write(b'++mode 1\n')
    ser.write(b'++auto 1\n')
    ser.write(b'++ver\n')
    response = ser.readline().decode().strip()  # Read and decode the response
    print("Prologix Version:", response)

    # talk to HP 34401
    ser.write(b'++addr 23\n')
    ser.write(b'*IDN?\n')
    s = ser.readline(256).decode().strip()
    if len(s) > 0:
        print('DVM: ',s)
    ser.write(b':READ?\n')
    s = ser.readline().decode().strip()
    s = s.replace(s[0], '', 1)
    if len(s) > 0:
        print('Data: ',s)

    # talk to HP 33120
    ser.write(b'++addr 9\n')
    ser.write(b'*IDN?\n')
    s = ser.readline().decode().strip()
    if len(s) > 0:
        print(s)
    ser.write(b':FREQ?\n')
    s = ser.readline().decode().strip()
    s = s.replace(s[0], '', 1)
    if len(s) > 0:
        print('Frequency: ',s)

    # talk to keithley 2400
        ser.write(b'++addr 24\n')
        ser.write(b'*IDN?\n')
        s = ser.readline().decode().strip()
        if len(s) > 0:
            print('SMU: ', s)
        ser.write(b':DISP:TEXT:DATA "ImsaiGuy"\n')
        ser.write(b':DISP:TEXT:STAT ON\n')
        s = ser.readline().decode().strip()
        if len(s) > 0:
            print('SMU: ', s)
        ser.write(b':OUTPut ON\n')
        s = ser.readline().decode().strip()
        if len(s) > 0:
            print(s)

        ser.write(b':READ?\n')
        s = ser.readline().decode().strip()
        # s = s.replace(s[0], '', 1)
        if len(s) > 0:
            print('Data: ', s)
        # remove first character in string

        numbers = s.strip().split(',')
        # Convert the numbers from strings to integers (or floats, if needed)
        num1, num2, num3, num4, num5 = map(float, numbers)  # Use float() if numbers can have decimals
        # Printing the parsed values
        print(f"Number 1: {num1}")
        print(f"Number 2: {num2}")
        print(f"Number 3: {num3}")
        print(f"Number 4: {num4}")
        print(f"Number 5: {num5}")

    ser.close()
else:
    print(f"Failed to open port")
