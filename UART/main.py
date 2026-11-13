
# main.py - Raspberry Pi Pico W
#
# Simple USB Serial Communication Protocol
#
# Protocol:
#   COMMAND[:VALUE]\n
#
# Every command receives exactly one response.
# All messages end with a newline (\n).
#
# Examples:
#
# Raspberry Pi sends:    PING\n
# Pico W responds:       OK:PONG\n
#
# Raspberry Pi sends:    TEMP\n
# Pico W responds:       OK:TEMP:24.65\n
#
# Raspberry Pi sends:    LED:ON\n
# Pico W responds:       OK:LED:ON\n
#
# Raspberry Pi sends:    LED:OFF\n
# Pico W responds:       OK:LED:OFF\n
#
# Raspberry Pi sends:    HELP\n
# Pico W responds:       OK:COMMANDS:PING,TEMP,LED,HELP\n
#
# Raspberry Pi sends:    ABC\n
# Pico W responds:       ERR:UNKNOWN_COMMAND\n
#
# Students can extend the protocol by adding
# additional commands to process_command().

import machine
import sys

# Hardware
sensor = machine.ADC(4)
led = machine.Pin("LED", machine.Pin.OUT)

# ADC conversion
CONVERSION_FACTOR = 3.3 / 65535


def read_temperature():
    raw = sensor.read_u16()
    voltage = raw * CONVERSION_FACTOR

    temperature = 27 - (voltage - 0.706) / 0.001721

    return temperature


def process_command(command):
    # Split message into command and optional value
    parts = command.split(":", 1)

    instruction = parts[0]
    value = parts[1] if len(parts) > 1 else ""

    # Test communication
    if instruction == "PING":
        return "OK:PONG"

    # Read temperature
    elif instruction == "TEMP":
        temperature = read_temperature()
        return "OK:TEMP:{:.2f}".format(temperature)

    # Control onboard LED
    elif instruction == "LED":
        if value == "ON":
            led.on()
            return "OK:LED:ON"

        elif value == "OFF":
            led.off()
            return "OK:LED:OFF"

        else:
            return "ERR:INVALID_VALUE"

    # Show available commands
    elif instruction == "HELP":
        return "OK:COMMANDS:PING,TEMP,LED,HELP"

    # Unknown command
    else:
        return "ERR:UNKNOWN_COMMAND"


def main():
    led.off()

    while True:
        # Receive a line from Raspberry Pi
        command = sys.stdin.readline().strip()

        if not command:
            continue

        # Execute command
        response = process_command(command)

        # Send response to Raspberry Pi
        print(response)


main()