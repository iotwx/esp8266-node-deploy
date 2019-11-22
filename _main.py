'''
efforts to implement bme680 on micropython:
https://github.com/robmarkcole/bme680-mqtt-micropython/tree/master/lib

circuitpython implementation:
https://github.com/adafruit/Adafruit_CircuitPython_BME680

mqtt implementation for circuitpython sucks for the 8266 (e.g. it won't work)!

LUCKILY the simple umqtt client works great and was ported here!
'''
from binascii import hexlify
from gc import collect, mem_alloc, mem_free, threshold
from time import sleep

import board
import machine
from busio import I2C
from ujson import load

from umqtt.simple import MQTTClient

# dynamically load the remaining device imports
with open('config.json') as f:
    config = load(f)

    CLIENT_ID = ''.join([chr(b) for b in hexlify(machine.unique_id())])
    MEASUREMENT_INTERVAL_SEC = config['measurement_interval_sec']

    collect()


def publish_measurement(node, dt, data, client_id=CLIENT_ID):
    client = MQTTClient(client_id, MQ_BROKER, port=MQ_PORT)
    client.connect()

    client.publish(
        'measurements',
        b"device: nodemcu/{}\ninstrument: {}\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'".format(
            client_id, node, dt, data, mem_alloc(), mem_free()
        ),
    )

    print(
        b"device: nodemcu/{}\ninstrument: {}\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'".format(
            client_id, node, dt, data, mem_alloc(), mem_free()
        )
    )
    collect()


def get_current_dt():
    y, m, dd, z, hh, mm, ss, _ = machine.RTC().datetime()
    return '{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}'.format(y, m, dd, hh, mm, ss)


if __name__ == '__main__':
    try:
        start_hour = machine.RTC().datetime()[4]
        threshold(1024 * 12)

        #     # set device time from network
        #     ntptime.settime()
        # BROKEN IN CIRCUITPYTHON! set time, WTF, ntptime crashes the
        # machine!!!

        # setup global variables
        MQ_BROKER = config['mqtt']['broker']
        MQ_PORT = config['mqtt']['port']
        INSTALLED_SENSORS = list(config['sensors'].keys())

        # set up i2c bus
        i2c = I2C(board.SCL, board.SDA)

        collect()

        if 'sgp30' in INSTALLED_SENSORS:
            import adafruit_sgp30

            sensor = adafruit_sgp30.Adafruit_SGP30(i2c)
            sensor.iaq_init()
            sensor.set_iaq_baseline(0x8973, 0x8AAE)
            collect()

        print(mem_free())
        while True:
            for device in INSTALLED_SENSORS:
                i2c = I2C(board.SCL, board.SDA)

                if device == 'bmp280':
                    import adafruit_bmp280

                    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
                    dt = get_current_dt()

                    publish_measurement('{}/temp'.format(device), dt, sensor.temperature)
                    publish_measurement('{}/pressure'.format(device), dt, sensor.pressure)

                    collect()

                if device == 'htu21d':
                    import adafruit_htu21d

                    sensor = adafruit_htu21d.HTU21D(i2c)
                    dt = get_current_dt()

                    publish_measurement('{}/temp'.format(device), dt, sensor.temperature)
                    publish_measurement('{}/humidity'.format(device), dt, sensor.pressure)

                    collect()

                if device == 'bme680':
                    import adafruit_bme680

                    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=118)
                    dt = get_current_dt()

                    publish_measurement('{}/temp', dt, sensor.temperature)
                    publish_measurement('{}/humidity', dt, sensor.humidity)
                    publish_measurement('{}/pressure', dt, sensor.pressure)
                    publish_measurement('{}/gas', dt, sensor.gas)
                    publish_measurement('{}/altitude', dt, sensor.altitude)
                    collect()

                if device == 'bme280':
                    import adafruit_bme280

                    sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=118)
                    dt = get_current_dt()

                    publish_measurement('{}/temp', dt, sensor.temperature)
                    publish_measurement('{}/humidity', dt, sensor.humidity)
                    publish_measurement('{}/pressure', dt, sensor.pressure)
                    publish_measurement('{}/altitude', dt, sensor.altitude)
                    collect()

                if device == 'mcp9808':
                    import adafruit_mcp9808

                    sensor = adafruit_mcp9808.MCP9808(i2c)
                    dt = get_current_dt()

                    publish_measurement('{}/temp', dt, sensor.temperature)
                    collect()

                if device == 'veml6070':
                    import adafruit_veml6070

                    sensor = adafruit_veml6070.VEML6070(i2c)
                    dt = get_current_dt()

                    publish_measurement('{}/gas', dt, sensor.read)
                    collect()

                if device == 'sgp30':
                    sensor = adafruit_sgp30.Adafruit_SGP30(i2c)

                    dt = get_current_dt()

                    publish_measurement('{}/eCO2', dt, sensor.eCO2)
                    publish_measurement('{}/TVOC', dt, sensor.TVOC)
                    collect()

                    print(
                        '**** Baseline values: eCO2 = {0x%x}, TVOC = {0x%x}'.format(
                            sensor.baseline_eCO2, sensor.baseline_TVOC
                        )
                    )

            sleep(MEASUREMENT_INTERVAL_SEC)

            # reset the chip after 3 hours
            if machine.RTC().datetime()[4] > start_hour + 2:
                machine.reset()
    except Exception as e:
        print('[fail] {}'.format(e))
        sleep(MEASUREMENT_INTERVAL_SEC / 10.0)
        machine.reset()
