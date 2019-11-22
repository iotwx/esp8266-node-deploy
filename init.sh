echo "*** MOVING config.json***"
ampy -p /dev/ttyUSB0 put _config.json config.json

echo "*** MOVING adafruit_sgp30.py ***"
ampy -p /dev/ttyUSB0 put sensor_files/adafruit_sgp30.mpy /adafruit_sgp30.mpy

echo "*** MOVING adafruit_bmp280.py ***"
ampy -p /dev/ttyUSB0 put sensor_files/adafruit_bmp280.mpy /adafruit_bmp280.mpy

echo "*** MOVING adafruit_bme280.py ***"
ampy -p /dev/ttyUSB0 put sensor_files/adafruit_bme280.mpy /adafruit_bme280.mpy

echo "*** MOVING adafruit_bme680.py ***"
ampy -p /dev/ttyUSB0 put sensor_files/adafruit_bme680.mpy /adafruit_bme680.mpy

echo "*** MOVING adafruit_htu21d.py ***"
ampy -p /dev/ttyUSB0 put sensor_files/adafruit_htu21d.mpy /adafruit_htu21d.mpy

echo "*** MOVING adafruit_veml6070-.py ***"
ampy -p /dev/ttyUSB0 put sensor_files/adafruit_veml6070.mpy /adafruit_veml6070.mpy

echo "*** MOVING adafruit_lsm303d.py ***"
ampy -p /dev/ttyUSB0 put sensor_files/adafruit_lsm303.mpy /adafruit_lsm303.mpy

echo "*** MOVING adafruit_mcp9808.py ***"
ampy -p /dev/ttyUSB0 put sensor_files/adafruit_mcp9808.mpy /adafruit_mcp9808.mpy

echo "*** MOVING adafruit_bus_device ***"
ampy -p /dev/ttyUSB0 mkdir /adafruit_bus_device
ampy -p /dev/ttyUSB0 put adafruit_bus_device/i2c_device.mpy /adafruit_bus_device/i2c_device.mpy
ampy -p /dev/ttyUSB0 put adafruit_bus_device/spi_device.mpy /adafruit_bus_device/spi_device.mpy
ampy -p /dev/ttyUSB0 put adafruit_bus_device/__init__.py /adafruit_bus_device/__init__.py

echo "*** MOVING lib umqtt package files ***"
ampy -p /dev/ttyUSB0 mkdir /umqtt
ampy -p /dev/ttyUSB0 put umqtt/simple.py /umqtt/simple.py
ampy -p /dev/ttyUSB0 put umqtt/__init__.py /umqtt/__init__.py
ampy -p /dev/ttyUSB0 put umqtt/robust.py /umqtt/robust.py

echo "*** MOVING main.py ***"
ampy -p /dev/ttyUSB0 put _main.py /_main.py

echo "*** MOVING boot.py ***"
ampy -p /dev/ttyUSB0 put _boot.py /_boot.py
