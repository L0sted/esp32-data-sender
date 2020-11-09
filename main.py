# This is your main script.
from machine import ADC, Pin
import time
start = time.ticks_ms()

sensor = ADC(Pin(32))
sensor.atten(ADC.ATTN_11DB)
# while True:
#     print(sensor.read())
#     time.sleep(0.2)

# import time, ds18x20, onewire
# ow = onewire.OneWire(Pin(27, Pin.IN, Pin.PULL_UP))
# ds = ds18x20.DS18X20(ow)
# roms = ds.scan()
# ds.convert_temp()
# time.sleep_ms(750)
# for rom in roms:
#     print(ds.read_temp(rom))

#read values
import dht, machine
print("reading temps...")
d = dht.DHT22(machine.Pin(27))
d.measure()
d.temperature() # eg. 23.6 (°C)
d.humidity()    # eg. 41.3 (% RH)
print("got dht22 values!\nconnecting to wifi...")

#connect to the wifi
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.scan()
if not wlan.isconnected():
    import pwd
    wlan.connect(pwd.ssid, pwd.pwd) # connect to an AP
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig(),"\tconnected!")
host_ip = "192.168.100.102"
print("connecting to server with ip", host_ip,"...")

#open socket
import usocket
sock = usocket.socket()
addr = usocket.getaddrinfo(host_ip, 8082)[0][-1]
sock.connect(addr)

print("compressing data into json and sending it...")
import ujson
payload = ujson.dumps(
    [d.temperature(), d.humidity(), sensor.read()]
)
sock.send(str(payload))
sock.close()
print("\tYAY! success! sent:\n", payload)

#bye bye
print("going to deep sleep")
# time.sleep(3)
print("Zzzz.... execution took: ", time.ticks_diff(time.ticks_ms(), start))
machine.deepsleep(900000)