'''
efforts to implement bme680 on micropython:
https://github.com/robmarkcole/bme680-mqtt-micropython/tree/master/lib

circuitpython implementation:
https://github.com/adafruit/Adafruit_CircuitPython_BME680

mqtt implementation for circuitpython sucks for the 8266 (e.g. it won't work)!

LUCKILY the simple umqtt client works great and was ported here!
'''
import machine
import binascii
import board
import busio
import gc
import time
import ujson
from umqtt.simple import MQTTClient

# dynamically load the remaining device imports
with open("config.json") as f:
    config = ujson.load(f)

    for device in config['sensors'].keys():
        module = config['sensors'][device]['driver']
        globals()[module] = __import__(module)
        print("imported {}".format(module))
        

def publish_measurement(node, dt, data, client_id=CLIENT_ID):
    client = MQTTClient(client_id, MQ_BROKER, port=MQ_PORT)
    client.connect()

    client.publish("measurements",
                    b"device: nodemcu/{}\ninstrument: {}\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'" \
                      .format(client_id, node, dt, data, gc.mem_alloc(), gc.mem_free()))
    
    print(b"device: nodemcu/{}\ninstrument: {}\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'" \
                      .format(client_id, node, dt, data, gc.mem_alloc(), gc.mem_free()))
    gc.collect()


def get_current_dt():
    y, m, dd, z, hh, mm, ss, _ = machine.RTC().datetime()
    return "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(y, m, dd, hh, mm, ss)


if __name__ == "__main__":
    try:
        start_hour = machine.RTC().datetime()[4]
        gc.threshold(1024*12)
        
        #     # set device time from network
        #     ntptime.settime()
        #     BROKEN IN CIRCUITPYTHON! set time, WTF, ntptime crashes the machine!!!

        # setup global variables
        MQ_BROKER = config['mqtt']['broker']
        MQ_PORT = config['mqtt']['port']
        INSTALLED_SENSORS = list(config['sensors'].keys())
        CLIENT_ID = ''.join([chr(b) for b in binascii.hexlify(machine.unique_id())])
        MEASUREMENT_INTERVAL_SEC = config['measurement_interval_sec']

        while True:
            for device in INSTALLED_SENSORS:
                i2c = busio.I2C(board.SCL, board.SDA)

                if device == "bmp280":
                    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
                    dt = get_current_dt()
                    
                    publish_measurement("{}/temp".format(device), dt, sensor.temperature)
                    publish_measurement("{}/pressure".format(device), dt, sensor.pressure)
                    
                    gc.collect()
                    
                if device == "htu21d":
                    sensor = adafruit_htu21d.HTU21D(i2c)
                    dt = get_current_dt()
                    
                    publish_measurement("{}/temp".format(device), dt, sensor.temperature)
                    publish_measurement("{}/humidity".format(device), dt, sensor.pressure)
                    
                    gc.collect()

                if device == "bme680":
                    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=118)
                    dt = get_current_dt()
                    
                    publish_measurement("{}/temp", dt, sensor.temperature)
                    publish_measurement("{}/humidity", dt, sensor.humidity)
                    publish_measurement("{}/pressure", dt, sensor.pressure)
                    publish_measurement("{}/gas", dt, sensor.gas)
                    publish_measurement("{}/altitude", dt, sensor.altitude)
                    gc.collect()

                if device == "bme280":
                    sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c)
                    dt = get_current_dt()
                    
                    publish_measurement("{}/temp", dt, sensor.temperature)
                    publish_measurement("{}/humidity", dt, sensor.humidity)
                    publish_measurement("{}/pressure", dt, sensor.pressure)
                    publish_measurement("{}/altitude", dt, sensor.altitude)
                    gc.collect()
                
                if device == "mcp9808":
                    sensor = adafruit_mcp9808.MCP9808(i2c_bus)
                    dt = get_current_dt()
                    
                    publish_measurement("{}/temp", dt, sensor.temperature)
                    gc.collect()

                if device == "veml6070":
                    sensor = adafruit_veml6070.VEML6070(i2c)
                    dt = get_current_dt()

                    publish_measurement("{}/gas", dt, sensor.read)
                    gc.collect()
                    
            time.sleep(MEASUREMENT_INTERVAL_SEC)

            # reset the chip after 3 hours
            if machine.RTC().datetime()[4] > start_hour+2:
                 machine.reset()
# 
#     
# 
# 
# try:     
#     MEASUREMENT_INTERVAL_SEC = 60
#     machine.RTC().datetime((2019, 10, 6, 11, 0, 0, 0, 0))
# 
#     i2c = busio.I2C(board.SCL, board.SDA)
# 
#     # connect to MQ broker
#     MQ_BROKER, MQ_PORT = 'pt2050dashboard-dev.tacc.utexas.edu', 1883
#     client_id = ''.join([chr(b) for b in binascii.hexlify(machine.unique_id())])
#     client = MQTTClient(client_id, MQ_BROKER, port=MQ_PORT)
#     client.connect()
#     
#     gc.threshold(1024*12)
#     
#     # loop over measurements
#     start_hour = machine.RTC().datetime()[4]
#     
#     while True:
#         y, m, dd, z, hh, mm, ss, _ = machine.RTC().datetime()
#         dt = "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(y, m, dd, hh, mm, ss)
# 
#         # bme680
#         sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=118)
#         
#         publish_measurement(client, client_id, "bme680/temp", dt, sensor.temperature)
#         publish_measurement(client, client_id, "bme680/humidity", dt, sensor.humidity)
#         publish_measurement(client, client_id, "bme680/pressure", dt, sensor.pressure)
#         publish_measurement(client, client_id, "bme680/gas", dt, sensor.gas)
#         publish_measurement(client, client_id, "bme680/altitude", dt, sensor.altitude)
# 
#         # bmp280
#         
#         # htu21d
#         
#         # mcp9808
#         
#         # veml6070
# 
# #         client.publish("measurements",
# #                         b"device: nodemcu/{}\ninstrument: bme680/temp\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'" \
# #                           .format(client_id, dt, sensor.temperature, gc.mem_alloc(), gc.mem_free()))
# # 
# #         client.publish("measurements",
# #                         b"device: nodemcu/{}\ninstrument: bme680/humidity\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'" \
# #                           .format(client_id, dt, sensor.humidity, gc.mem_alloc(), gc.mem_free()))
# # 
# #         client.publish("measurements",
# #                         b"device: nodemcu/{}\ninstrument: bme680/pressure\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'" \
# #                           .format(client_id, dt, sensor.pressure, gc.mem_alloc(), gc.mem_free()))
# # 
# #         client.publish("measurements",
# #                         b"device: nodemcu/{}\ninstrument: bme680/gas\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'" \
# #                           .format(client_id, dt, sensor.gas, gc.mem_alloc(), gc.mem_free()))
# # 
# #         client.publish("measurements",
# #                         b"device: nodemcu/{}\ninstrument: bme680/altitude\nd: '{}'\nm: {}\nmemory: '<alloc:{} free:{}>'" \
# #                           .format(client_id, dt, sensor.altitude, gc.mem_alloc(), gc.mem_free()))
# 
#         time.sleep(MEASUREMENT_INTERVAL_SEC)
#         
#         # reset the machine every 2 hours
#         if machine.RTC().datetime()[4] > start_hour+2:
#             machine.reset()
# 
    except Exception as e:
        print("[fail] {}".format(e))
        time.sleep(MEASUREMENT_INTERVAL_SEC / 10.)
        machine.reset()
