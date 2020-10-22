
import time

import pigpio
from pisat.handler import PigpioDigitalInputHandler

from camera import FlightCamera


def test_flight_camera():
    
    PIN = 17
    
    pi = pigpio.pi()
    handler = PigpioDigitalInputHandler(pi, PIN, pulldown=True)
    camera = FlightCamera(handler)
    
    camera.start_record(blocking=False)
    time.sleep(10)
    camera.stop_record()
    
    
if __name__ == "__main__":
    test_flight_camera()
