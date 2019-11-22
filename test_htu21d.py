import busio
import board
import adafruit_htu21d

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_htu21d.HTU21D(i2c)