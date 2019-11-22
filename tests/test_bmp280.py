# import adafruit_bmp280
import adafruit_bmp280
import adafruit_htu21d
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
sensor2 = adafruit_htu21d.HTU21D(i2c)
