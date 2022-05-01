import I2C_LCD_driver

def LCD_display(message, line, position):
    mylcd = I2C_LCD_driver.lcd()
    mylcd.lcd_display_string(message, line, position)
