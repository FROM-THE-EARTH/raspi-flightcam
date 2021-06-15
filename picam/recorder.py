from __future__ import annotations
import os
import time
import threading
import typing as t

import picamera
from pisat.handler import DigitalInputHandlerBase
from pisat.util.about_time import get_time_stamp

from .utils import IterSingleton


_INF = float("inf")


class _GPIOPins(IterSingleton[int]):

    GPIO00 = 0
    GPIO01 = 1
    GPIO02 = 2
    GPIO03 = 3
    GPIO04 = 4
    GPIO05 = 5
    GPIO06 = 6
    GPIO07 = 7
    GPIO08 = 8
    GPIO09 = 9
    GPIO10 = 10
    GPIO11 = 11
    GPIO12 = 12
    GPIO13 = 13
    GPIO14 = 14
    GPIO15 = 15
    GPIO16 = 16
    GPIO17 = 17
    GPIO18 = 18
    GPIO19 = 19
    GPIO20 = 20
    GPIO21 = 21
    GPIO22 = 22
    GPIO23 = 23
    GPIO24 = 24
    GPIO25 = 25
    GPIO26 = 26

    GPIO_MIN = GPIO00
    GPIO_MAX = GPIO26


class _VideoFormats(IterSingleton[str]):

    h264    = "h264"
    mjpeg   = "mjpeg"
    yuv     = "yuv"
    rgb     = "rgb"
    rgba    = "rgba"
    bgr     = "bgr"
    bgra    = "bgra"


GPIOPins = _GPIOPins()
VideoFormats = _VideoFormats()


def isvalid_video_format(path: str) -> bool:
    ext = os.path.splitext(path)[1]
    if not len(ext):
        return False
    return ext[1:] in VideoFormats


class IORecorder:

    def __init__(
        self,
        handler: DigitalInputHandlerBase,
        fname: t.Optional[str] = None,
        resolution: t.Tuple = (640, 480)
    ) -> None:
        if fname is None:
            fname = get_time_stamp("mov", "h264")
        elif isvalid_video_format(fname):
            raise ValueError(f"'{fname}' has an invalid extension.")

        self._camera = picamera.PiCamera()
        self._camera.resolution = resolution
        self._fname = fname
        self._handler: DigitalInputHandlerBase = handler

    @property
    def is_high(self) -> bool:
        return self._handler.observe()

    def start_record(
        self,
        interval: float = 1.,
        timeout: float = -1,
        start_with_low: bool = False,
    ) -> None:
        if timeout <= 0:
            timeout = _INF
        if start_with_low:
            while self.is_high:
                pass

        self._flag = False
        self._camera.start_recording(self._fname)

        time_init = time.time()
        try:
            while not self.state and not self._flag:
                if time.time() - time_init >= timeout:
                    break
                self._camera.wait_recording(timeout=interval)
        finally:
            self._camera.stop_recording()


class ThreadingIORecorder(IORecorder):

    def __init__(
        self,
        handler: DigitalInputHandlerBase,
        fname: t.Optional[str] = None,
        resolution: t.Tuple = (640, 480),
    ) -> None:
        super().__init__(handler, fname=fname, resolution=resolution)

        self._handler: DigitalInputHandlerBase = handler
        self._thread: t.Optional[threading.Thread] = None

    def start_record(
        self,
        interval: float = 1.,
        timeout: float = -1,
        start_with_low: bool = False,
    ) -> ThreadingIORecorder:
        self._thread = threading.Thread(
            target=super().start_record,
            args=(interval, timeout, start_with_low),
        )
        self._thread.start()
        return self

    def stop_record(self, timeout: float = -1) -> bool:
        if self._thread is None:
            return

        self._flag = True
        self._thread.join(timeout=timeout)

        if not self._thread.is_alive():
            self._flag = False
        return self._flag

    def __enter__(self) -> ThreadingIORecorder:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stop_record()
