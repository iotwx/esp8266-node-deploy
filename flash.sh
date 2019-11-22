echo "*** ERASING DEVICE***"
esptool.py --port /dev/ttyUSB0 erase_flash

echo "*** FLASHING MICROKERNEL ***"
esptool.py --port /dev/ttyUSB0 --baud 57600 write_flash --flash_size=detect -fm dio 0 adafruit-circuitpython-feather_huzzah-3.1.2.bin 




