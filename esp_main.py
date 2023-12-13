import socket
import network
from machine import Pin
import time
from machine import ADC

ssid = 'YNWA'
password = '123456789'
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    time.sleep(1)
    
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server_address = ('192.168.137.142', 12345)
server_address = ('192.168.137.142', 12345)
udp_socket.bind(('0.0.0.0', 12345))

pir = Pin(14, Pin.IN, Pin.PULL_UP)
sensor = ADC(Pin(36))
sensor.width(ADC.WIDTH_10BIT)
sensor.atten(ADC.ATTN_11DB)
led = Pin(12, Pin.OUT,value=0)

while True:
    lightvalue = sensor.read()
    pirVal = pir.value()

    time.sleep(2)
    if pirVal == 1:
        print("Beboeren står op")
        message = "Beboeren står op"
        udp_socket.sendto(message.encode(), server_address)
        time.sleep(1)
        if lightvalue <= 150:
            print("Der er mørkt lys tændes")
            message = "Der er mørkt lys tændes"
            udp_socket.sendto(message.encode(), server_address)
            led.value(1)
            time.sleep(4)
            led.value(0)
            

