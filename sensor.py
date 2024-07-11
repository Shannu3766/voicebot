import RPi.GPIO as GPIO
import time
import pygame
from RPLCD.i2c import CharLCD
from time import sleep
import board
import adafruit_dht

lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

MQ_SENSOR_PIN = 17
DHT_PIN = 4

GPIO.setup(MQ_SENSOR_PIN, GPIO.IN)

dht_device = adafruit_dht.DHT11(board.D4)

pygame.mixer.init()
pygame.mixer.music.load("alert_sound.mp3")

THRESHOLD = 1


def alert():
    lcd.cursor_pos = (1, 0)
    lcd.write_string('Fire Alert..')
    pygame.mixer.music.play()


try:
    while True:
        sensor_value = GPIO.input(MQ_SENSOR_PIN)
        print(f"MQ Sensor Value: {sensor_value}")
        if sensor_value == 0:
            print("Threshold exceeded! Alert!")
            alert()
            time.sleep(8)
            lcd.clear()

        try:
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f'Temp: {temperature_c:.1f} C')
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f'Humidity: {humidity:.1f} %')
        except RuntimeError as e:
            print(f"Error reading DHT11 sensor: {e}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Program terminated by user")

finally:
    GPIO.cleanup()
    pygame.mixer.quit()
    lcd.clear()
