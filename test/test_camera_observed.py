
import time

import pigpio
from pisat.handler import PigpioDigitalInputHandler

from camera import FlightCamera


def main():

    PIN = 17

    pi = pigpio.pi()
    handler = PigpioDigitalInputHandler(pi, PIN, pulldown=True)
    camera = FlightCamera(handler)

    camera.start_record()


if __name__ == "__main__":
    main()
