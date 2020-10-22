
import argparse
from socket import timeout
from typing import Optional, Tuple

import pigpio
from pisat.handler import PigpioDigitalInputHandler

from camera import FlightCamera


class classproperty(property):
    pass

class PropertyMeta(type):
    
    def __new__(cls, name, bases, namespace):
        properties = {key: val for key, val in namespace.items() if type(val) == classproperty}
        for key, val in properties.items():
            setattr(cls, key, val)
            del namespace[key]
                
        return type.__new__(cls, name, bases, namespace)

class CameraArgs(metaclass=PropertyMeta):
    
    OPTION_PIN = "--pin"
    OPTION_PIN_S = "-p"
    OPTION_INTERVAL = "--interval"
    OPTION_INTERVAL_S = "-i"
    OPTION_TIMEOUT = "--timeout"
    OPTION_TIMEOUT_S = "-t"
    OPTION_FNAME = "--fname"
    OPTION_FNAME_S = "-f"
    OPTION_RESOLUTION = "--resolution"
    OPTION_RESOLUTION_S = "-r"
    
    DEFAULT_PIN: int = 17
    DEFAULT_INTERVAL: float = 1.
    DEFAULT_TIMEOUT: Optional[float] = None
    DEFAULT_FNAME: Optional[str] = None
    DEFAULT_RESOLUTION: Tuple[int] = (640, 480)
    
    SEPARATOR_RESOLUTION = ":"
    
    _pin = DEFAULT_PIN
    _interval = DEFAULT_INTERVAL
    _timeout = DEFAULT_TIMEOUT
    _fname = DEFAULT_FNAME
    _resolution = DEFAULT_RESOLUTION
    
    @classproperty
    def pin(cls):
        return cls._pin

    @classproperty
    def interval(cls):
        return cls._interval
    
    @classproperty
    def timeout(cls):
        return cls._timeout
        
    @classproperty
    def fname(cls):
        return cls._fname

    @classproperty
    def resolution(cls):
        return cls._resolution
    
    @classmethod
    def format_pin(cls, pin: Optional[str]) -> int:
        if pin is not None:
            try:
                pin = int(pin)
                
                if 1 <= pin <= 26:
                    cls._pin = pin
                else:
                    raise ValueError(
                        f"'{cls.OPTION_PIN}' must be 1 <= 'pin' <= 26."
                    )
            except:
                raise ValueError(
                    f"'{cls.OPTION_PIN}' must be convertable into int."
                )
        return cls.pin
    
    @classmethod
    def format_interval(cls, interval: Optional[str]) -> float:
        if interval is not None:
            try:
                interval = float(interval)
                if interval > 0.:
                    cls._interval = interval
                else:
                    raise ValueError(
                        f"'{cls.OPTION_INTERVAL}' must be bigger than 0."
                    )
            except:
                raise ValueError(
                    f"'{cls.OPTION_INTERVAL}' must be convertable into float."
                )
        
        return cls.interval
    
    @classmethod
    def format_timeout(cls, timeout: Optional[str]) -> Optional[float]:
        if timeout is not None:
            try:
                timeout = float(timeout)
                if timeout > 0.:
                    cls._timeout = timeout
                else:
                    raise ValueError(
                        f"'{cls.OPTION_INTERVAL}' must be bigger than 0."
                    )
            except:
                raise ValueError(
                    f"'{cls.OPTION_TIMEOUT}' must be convertable into float" +
                    "if not None."
                )
        return cls.timeout
    
    @classmethod
    def format_fname(cls, fname: Optional[str]) -> Optional[str]:
        if fname is not None:
            cls._fname = fname
        return cls.fname
    
    @classmethod
    def format_resolution(cls, resolution: Optional[str]) -> Tuple[int]:
        if resolution is not None:
            resolution = resolution.split(cls.SEPARATOR_RESOLUTION)
            if len(resolution) != 2:
                raise ValueError(
                    f"'{cls.OPTION_RESOLUTION}' must be represented using " +
                    f"'{cls.SEPARATOR_RESOLUTION}, 'such like 'width:height'."
                )
                
            try:
                for i, val in enumerate(resolution):
                    resolution[i] = int(val)
                cls._resolution = tuple(resolution)
            except:
                raise ValueError(
                    f"Each elements of '{cls.OPTION_RESOLUTION}' must be "+
                    "convertable into int."
                )
        return cls.resolution


def main(pin: int = 17, 
         interval: float = 1.,
         timeout: Optional[float] = None,
         fname: Optional[str] = None,
         resolution: Tuple = (640, 480)):

    pi = pigpio.pi()
    handler = PigpioDigitalInputHandler(pi, pin, pulldown=True)
    camera = FlightCamera(handler, fname=fname, resolution=resolution)

    camera.start_record(interval=interval, timeout=timeout)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(CameraArgs.OPTION_PIN_S, 
                        CameraArgs.OPTION_PIN, 
                        type=CameraArgs.format_pin)
    parser.add_argument(CameraArgs.OPTION_INTERVAL_S, 
                        CameraArgs.OPTION_INTERVAL, 
                        type=CameraArgs.format_interval)
    parser.add_argument(CameraArgs.OPTION_TIMEOUT_S, 
                        CameraArgs.OPTION_TIMEOUT, 
                        type=CameraArgs.format_timeout)
    parser.add_argument(CameraArgs.OPTION_FNAME_S, 
                        CameraArgs.OPTION_FNAME, 
                        type=CameraArgs.format_fname)
    parser.add_argument(CameraArgs.OPTION_RESOLUTION_S, 
                        CameraArgs.OPTION_RESOLUTION, 
                        type=CameraArgs.format_resolution)
    
    args = parser.parse_args()
    
    main(pin=CameraArgs.pin,
         interval=CameraArgs.interval,
         timeout=CameraArgs.timeout,
         fname=CameraArgs.fname,
         resolution=CameraArgs.resolution)
