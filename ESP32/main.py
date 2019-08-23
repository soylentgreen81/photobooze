import network
import usocket as socket
from machine import Pin
from time import sleep

# Setup
wlan = network.WLAN(network.STA_IF)
status_led = Pin(2, Pin.OUT)

led_red = Pin(21, mode=Pin.OUT)
led_green = Pin(22, mode=Pin.OUT)
led_blue  = Pin(23, mode=Pin.OUT)

buzzer_button = Pin(18, mode=Pin.IN)
buzzer_led = Pin(19, mode=Pin.OUT)

def _connect_wifi():
    print("connecting")
    wlan.active(True)
    wlan.connect('photobooze')
    t=0.2
    dt = 0
    while not wlan.isconnected():
        status_led.on()
        sleep(t)
        status_led.off()
        sleep(t)
        dt += 2*t
        if dt >= 10 and dt < 20:
            print("das wird nichts mehr ...")
        elif dt >= 20:
            print("gib es auf ...")
            dt = 0 
    status_led.on()

def get_dates():
    if not wlan.isconnected():
        _connect_wifi()
    s=socket.socket()
    ai = socket.getaddrinfo("dates.damniam.de", 80)
    addr = ai[0][-1]
    s.connect(addr)
    s.send(b"GET / HTTP/1.0\r\nHOST: dates.damniam.de\r\n\r\n")
    print(s.recv(4096))
    s.close()
    del s

_connect_wifi()

def rgb_off():
    led_red.off()
    led_green.off()
    led_blue.off()

def rgb_on():
    led_red.on()
    led_green.on()
    led_blue.on()

def do_nothing(gpio_number):
    pass

def photo_request(gpio_number):
    buzzer_button.irq( trigger=Pin.IRQ_RISING, handler=do_nothing )
    print("cheeeese!!!")
    rgb_on()
    for t in range(10):
        buzzer_led.on()
        sleep(0.05)
        buzzer_led.off()
        sleep(0.05)
    rgb_off()
    buzzer_button.irq( trigger=Pin.IRQ_RISING, handler=photo_request )

# Test


buzzer_button.irq( trigger=Pin.IRQ_RISING, handler=photo_request )
