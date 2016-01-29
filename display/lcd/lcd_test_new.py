import time
import pylcdlib
lcd = pylcdlib.lcd(0x27,1)

#lcd.lcd_clear()
lcd.lcd_puts("Hello",1) #display "Hello" on line 1
lcd.lcd_puts("World!",2) #display "World!" on line 2
time.sleep(2)
lcd = pylcdlib.lcd(0x27,1)

