
import ultrasound
import board
import digitalio
import time
import board
import busio
import e5

SENSOR_PIN = board.GP1 # Pico W, MakeZurich Badge

if __name__ == '__main__':
    sonar = ultrasound.GroveUltrasonicRanger(SENSOR_PIN)

    btn = digitalio.DigitalInOut(board.GP3)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    btn_previous_state = True
    
    ir = digitalio.DigitalInOut(board.GP27)
    ir.direction = digitalio.Direction.INPUT

    led = digitalio.DigitalInOut(board.GP21)
    led.direction = digitalio.Direction.OUTPUT

    uart = busio.UART(board.GP4, board.GP5, baudrate=9600)
    lora_module = e5.LoRaModule(uart)
    
    print('Detecting distance...')
    
    while True:
        btn_current_state = btn.value
    # Only handling button key press down (if button is pressed then voltage on the pin is low, which equals to False)
        if btn_current_state != btn_previous_state and btn_current_state == False:
            led.value = not led.value
            print("\nButton was pressed")
            
            s_dist = sonar.get_distance()
            ir_value = ir.value
            
            print(f'ultrasound detector value: {s_dist} cm')
            lora_module.send(s_dist)
        
            print(f'infrared detector value: {ir_value}')
            lora_module.send(ir_value)
            
            time.sleep(1)
        
        btn_previous_state = btn_current_state
        time.sleep(1)

        



