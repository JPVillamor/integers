import time
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_tca9548a

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import adafruit_lsm9ds1

import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep
import adafruit_mlx90640

#i2c = board.I2C()  # uses board.SCL and board.SDA
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)


PRINT_TEMPERATURES = False
PRINT_ASCIIART = True
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768



# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)



sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)



led = LED(19)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN =26
GPIO.setup(PIR_PIN, GPIO.IN)



tca = adafruit_tca9548a.TCA9548A(i2c)

# Initialize Counters
StaleCount = 0
ValidCount = 0
FaultCount = 0

# Constants
FX29LoadRange  = 50    # Load Range for Force Sensor
FX29ZeroForce  = 800   # 0% Force Sensor Reading (Count)
FX29FullForce  = 15000  # 100% Force Sensor Reading (Count)

#IO variables
Command = bytearray(1)
F1Result  = bytearray(2)

#device = I2CDevice(i2c, 0x28)
force1 = I2CDevice(tca[0], 0x28)
force2 = I2CDevice(tca[1], 0x28)
force3 = I2CDevice(tca[6], 0x28)
force4 = I2CDevice(tca[7], 0x28)
f1name = 'force1'
f2name = 'force2'
f3name = 'force3'
f4name = 'force4'
def function(force1, fname):
    global StaleCount
    global ValidCount
    global FaultCount
    while True:
        try:
                # read command was used to retrieve a sensor reading
                force1.readinto(F1Result)

                # Handle Status information
                Status = ( F1Result[0] & 0xC0 ) >> 6
                if ( Status == 0 ) :
                    ValidCount = ValidCount + 1
                elif (Status == 2 ) :
                    StaleCount = StaleCount + 1
                elif (Status == 3 ) :
                    FaultCount = FaultCount + 1

                # Combine the two bytes of data after masking the Status bits into a single value
                Measurement = (( F1Result[0] & 0x3F ) << 8 | ( F1Result[1] & 0xFF ) )              # Reading from Device
                # Convert to lb without removing offset (FX29ZeroForce) from the Measurement.
                # Correct translation would be:
                # Force_lb = ((Measurement - FX29ZeroForce) * FX29LoadRange ) / (FX29FullForce - FX29ZeroForce)
                Force_lb    = (Measurement - FX29ZeroForce) * FX29LoadRange / (FX29FullForce - FX29ZeroForce)    # Converted to Pounds (lb)

                # Convert to grams
                Force_grm   = Force_lb * 453.59237                                             # Converted to grams  (g)

                # Remove decimals prior to reporting reading
                Force_Send  = int(Force_grm)                                                   # Reported Force (grams, no fraction)

                #initiate next measurement
                force1.readinto(Command)

                # Report Force
                print(fname + ' ' + str(Measurement))

                # Target a refresh rate of 100Hz
                time.sleep(.01)

                # Debug
                #print(FaultCount, StaleCount, ValidCount, Force_Send, Force_lb, Force_grm)
                break;
        except:
                # Handle IO exception by waiting it out
                time.sleep(0.010)
                #print("Exception")


while True:
    
   
    
     # Read acceleration, magnetometer, gyroscope, temperature.
    accel_x, accel_y, accel_z = sensor.acceleration
    mag_x, mag_y, mag_z = sensor.magnetic
    gyro_x, gyro_y, gyro_z = sensor.gyro
    temp = sensor.temperature
    # Print values.
    print(
        "Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})".format(
            accel_x, accel_y, accel_z
        )
    )
    print(
        "Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})".format(mag_x, mag_y, mag_z)
    )
    print(
        "Gyroscope (rad/sec): ({0:0.3f},{1:0.3f},{2:0.3f})".format(
            gyro_x, gyro_y, gyro_z
        )
    )
    print(": {0:0.2f}C".format(temp-.5))
    # Delay for a second.
    #time.sleep(0.1)
    
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    print("{:>5}\t{:>5.3f}".format(chan.value, chan1.voltage))
    print("{:>5}\t{:>5.3f}".format(chan.value, chan2.voltage))
    #print("{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
    print("")
    
    #time.sleep(0.5)
    
      
    with force1:
        function(force1, f1name)
    with force2:
        function(force2, f2name)
    with force3:
        function(force3, f3name)
    with force4:
        function(force4, f4name)
        print("")
        
        
    if GPIO.input(PIR_PIN):
     print('Motion Detected')
     led.on()
    else:
     led.off()
     print ('Ready')
    
    
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue
    print("Read 2 frames in %0.2f s" % (time.monotonic() - stamp))
    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            if PRINT_TEMPERATURES:
                print("%0.1f, " % t, end="")
            if PRINT_ASCIIART:
                c = "&"
                # pylint: disable=multiple-statements
                if t < 20:
                    c = " "
                elif t < 23:
                    c = "."
                elif t < 25:
                    c = "-"
                elif t < 27:
                    c = "*"
                elif t < 29:
                    c = "+"
                elif t < 31:
                    c = "x"
                elif t < 33:
                    c = "%"
                elif t < 35:
                    c = "#"
                elif t < 37:
                    c = "X"
                # pylint: enable=multiple-statements
                print(c, end="")
        print()
    print()