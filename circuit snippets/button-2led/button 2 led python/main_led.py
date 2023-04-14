from arduino_functions import *
import time

board = setup('/dev/tty.usbmodem1201')

# specifichiamo i pin dei collegamenti sulla board
button = get_digital_pin(board, 2)
green_led = get_digital_pin(board, 8)
red_led = get_digital_pin(board, 4)

# impostiamo la modalità del bottone su INPUT (necessario per leggere il bottone)
button.mode = pyfirmata.INPUT

green_led_state, red_led_state, last_button_value = False, False, False

# loop del programma
while True:
    # legge il valore del bottone (True o False)
    button_value = button.read()
    # controlla se il valore del bottone è cambiato
    if last_button_value != button_value:
        if button_value is True:
            # se lo stato del led verde è spento
            if green_led_state is False:
                green_led_state = True
                red_led_state = False
            else:
                green_led_state = False
                red_led_state = True

        time.sleep(0.1)
    # aggiorna ultimo valore del bottone
    last_button_value = button_value

    # se lo stato del led verde è acceso allora accende il led verde
    if green_led_state is True:
        green_led.write(1)
    else:  # altrimenti lo spegne
        green_led.write(0)

    if red_led_state is True:
        red_led.write(1)
    else:
        red_led.write(0)
