import busio
import board
# import adafruit_bmp280
globals()["adafruit_bmp280"] = __import__("adafruit_bmp280")
globals()["adafruit_htu21d"] = __import__("adafruit_htu21d")


i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
sensor2 = adafruit_htu21d.HTU21D(i2c)
