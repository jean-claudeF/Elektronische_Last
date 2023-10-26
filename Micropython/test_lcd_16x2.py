"""Example using a character LCD connected to an ESP8266 or Pico."""

from time import sleep
from lcdlib import CharLCD

lcd = CharLCD(rs=16, en=17, d4=18, d5=19, d6=20, d7=21,
				  cols=8, rows=2)

def hello_world():
	 # Print a 2 line centered message
	lcd.message('Hello', 2)
	lcd.set_line(1)
	lcd.message('World!', 2)

def lcd_values():
    lcd.message("500W at 10.2A")
    lcd.set_cursor(0, 1)
    lcd.message("20.3V at 10.2A")

lcd_values()
