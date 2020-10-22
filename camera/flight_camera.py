
import time
import threading
from typing import Optional, Tuple, Union

import picamera

from pisat.handler import DigitalInputHandlerBase
from pisat.util import get_time_stamp


class FlightCamera:
    
    def __init__(self, 
                 handler: DigitalInputHandlerBase,
                 fname: Optional[str] = None,
                 resolution: Tuple = (640, 480)) -> None:
        if not isinstance(handler, DigitalInputHandlerBase):
            raise TypeError(
                "'handler' must be DigitalInputHandlerBase."
            )
        
        if fname is None:
            fname = get_time_stamp("mov", "h264")
            
        if isinstance(resolution, tuple):
            if len(resolution) != 2:
                raise ValueError(
                    "size of 'resolution' must be 2."
                )
        else:
            raise TypeError(
                "'resolution' must be tuple."
            )
                    
        self._handler: DigitalInputHandlerBase = handler
        self._fname: str = fname
        self._camera = picamera.PiCamera()
        self._flag: bool = False
        self._thread = None
        
        self._camera.resolution = resolution
        
    @property
    def state(self):
        return self._handler.observe()
                
    def start_record(self, 
                     interval: Union[int, float] = 1.,
                     timeout: Optional[Union[int, float]] = None,
                     blocking: bool = True) -> None:
        if not isinstance(interval, (int, float)):
            raise TypeError(
                "'interval' must be int or float."
            )
        if not (isinstance(timeout, (int, float)) or timeout is None):
            raise TypeError(
                "'timeout' must be int, float or None."
            )
        
        if blocking:
            self._start_record(interval=interval)
        else:
            self._thread = threading.Thread(target=self._start_record, kwargs={"interval": interval})
            self._thread.start()
            
    def _start_record(self, 
                      interval: Union[int, float] = 1.,
                      timeout: Optional[Union[int, float]] = None):
        self._flag = False
        self._camera.start_recording(self._fname)
        
        try:
            if timeout is not None:
                while not self.state and not self._flag:
                    self._camera.wait_recording(timeout=interval)
            else:
                time_init = time.time()
                while not self.state and not self._flag:
                    if time.time() - time_init >= timeout:
                        break
                    self._camera.wait_recording(timeout=interval)
        finally:
            self._camera.stop_recording()
    
    def stop_record(self, timeout: Optional[float] = None) -> None:
        if self._thread is not None:
            self._flag = True
            self._thread.join(timeout=timeout)
            self._flag = False
