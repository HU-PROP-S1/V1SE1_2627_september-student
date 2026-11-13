
# pico_client.py - Raspberry Pi 4B
# This file is not for your Raspberry Pi Pico W but for your Raspberry Pi 4B!!!!!
#
# Interactive USB serial client.
#
# Example:
#
# User enters:       TEMP
# Pi sends:          TEMP\n
# Pico responds:     OK:TEMP:24.65\n
#
# User enters:       LED:ON
# Pi sends:          LED:ON\n
# Pico responds:     OK:LED:ON\n

import serial

PORT = "/dev/ttyACM0"
BAUDRATE = 115200


def send_command(pico, command):
    # Remove newline characters from user input
    command = command.strip()

    # Append newline to complete protocol message
    message = command + "\n"

    # Send command
    pico.write(message.encode("utf-8"))

    # Wait for response
    response = pico.readline().decode(
        "utf-8", errors="replace"
    ).strip()

    return response


def main():
    with serial.Serial(
        port=PORT,
        baudrate=BAUDRATE,
        timeout=2
    ) as pico:

        print("Connected to Pico W")
        print("Type HELP for commands")
        print("Type QUIT to exit")

        while True:
            command = input("\nCommand > ").strip()

            if command.upper() == "QUIT":
                break

            if not command:
                continue

            # Clear stale responses
            pico.reset_input_buffer()

            response = send_command(pico, command)

            if response:
                print("Pico >", response)
            else:
                print("ERROR: No response (timeout)")


if __name__ == "__main__":
    main()