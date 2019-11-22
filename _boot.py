# This file is executed on every boot (including wake-boot from deepsleep)
import machine
import time
import gc
gc.collect()

# connect the node to the network
import network
import ujson

try:
    with open("config.json") as f:
        config = ujson.load(f)
        
        ssid = config['network']['ssid']
        passwd = config['network']['password']

        # Create Station interface
        wlan = network.WLAN(network.STA_IF) 

        if not wlan.isconnected():
          print('Connecting...')

          # Enable the interface
          wlan.active(True)
                  
          # Connect
          print(ssid, passwd)
          wlan.connect(ssid, passwd)
          
          # Wait till connection is established
          while not wlan.isconnected():
               time.sleep(300)

          print('It is now connected.')

        else:
          print('Already Connected.')   

        print('Network Settings:', wlan.ifconfig())
except Exception as e:
    print("Network setup failed: {}".format(e))
