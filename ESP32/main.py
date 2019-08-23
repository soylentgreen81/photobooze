import network
import usocket as socket
from machine import Pin, Timer, PWM
import machine
from switch import Switch
import time
import _thread
import math

# Setup
wlan = network.WLAN(network.STA_IF)
status_led = Pin(2, Pin.OUT)

led_red = Pin(21, mode=Pin.OUT)
led_green = Pin(22, mode=Pin.OUT)
led_blue  = Pin(23, mode=Pin.OUT)
buzzer_button = Pin(18, mode=Pin.IN, pull=Pin.PULL_UP)
buzzer_led = Pin(19, mode=Pin.OUT)
buzzer_pwm = PWM(buzzer_led, freq=1000)

def _connect_wifi():
    print("connecting")
    led_blue.on()
    led_green.off()
    wlan.active(True)
    wlan.connect('photobooze')
    pulse(buzzer_pwm, 50, 1)
    t=0.2
    dt = 0
    while not wlan.isconnected():
        led_red.on()
        time.sleep(t)
        led_red.off()
        time.sleep(t)
        dt += 2*t
        if dt >= 10 and dt < 20:
            print("das wird nichts mehr ...")
        elif dt >= 20:
            print("gib es auf ...")
            dt = 0 
    status_led.on()
    led_blue.off()
    led_red.off()
    led_green.on()

def pulse(l, t, times):
    _thread.start_new_thread(pulse_thread, (l,t,times,))
def pulse_thread(led, pause, times):
    for n in range(times):
        for i in range(20):
            led.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
            time.sleep_ms(pause)
    led.duty(0)
def take_photo():
    if not wlan.isconnected():
        _connect_wifi()
    s=socket.socket()
    ai = socket.getaddrinfo("photobooze.org", 80)
    addr = ai[0][-1]
    print("connection to photobooze...")
    s.connect(addr)
    print("sending request...")
    s.send(b"GET /api/v1/trigger HTTP/1.0\r\nHOST: photobooze.org\r\n\r\n")
    print(s.recv(4096))
    s.close()
    del s


def rgb_off():
    led_red.off()
    led_green.off()
    led_blue.off()

def rgb_on():
    led_red.on()
    led_green.on()
    led_blue.on()

def request_photo():
    buzzer_led.on()
    pulse(buzzer_pwm, 50, 5)
    time.sleep(0.1)
    take_photo()
    buzzer_led.off()

def main():
    my_switch = Switch(buzzer_button)
    while True:

        my_switch_new_value = False
        # Disable interrupts for a short time to read shared variable
        irq_state = machine.disable_irq()
        if my_switch.new_value_available:
            my_switch_value = my_switch.value
            my_switch_new_value = True
            my_switch.new_value_available = False
        machine.enable_irq(irq_state)
 
        # If my switch had a new value, print the new state
        if my_switch_new_value:
            print("new value")
            if not my_switch_value:
                request_photo()
#while True:
#    sleep(0.1)
#    if buzzer_button.value() == 1:
#        photo_request()

print("starting up")
_connect_wifi()
main()

#buzzer_button.irq( trigger=Pin.IRQ_FALLING, handler=photo_request )
