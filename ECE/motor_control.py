import board
import busio
import adafruit_pca9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 50
left_motor = pca.channels[2]
right_motor = pca.channels[3]

MIN_WIDTH = 0xe14
MAX_WIDTH = 0x1852

PWM_RANGE = int((MAX_WIDTH - MIN_WIDTH) / 2)


# val in range -1 to 1
# -1 to 0: Reverse
# 0 to 1: Forward
# 0: Stop
def move_motors(left,right):
	if(left > 1):
		left = 1
	elif(left < -1):
		left = -1	
	if(right > 1):
		right = 1
	elif(right < -1):
		right = -1

	left_motor.duty_cycle = int(left * PWM_RANGE + MIN_WIDTH + PWM_RANGE)
	right_motor.duty_cycle = int(right * PWM_RANGE + MIN_WIDTH + PWM_RANGE)
