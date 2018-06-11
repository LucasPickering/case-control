import serial

from cc_core import logger
from cc_core.resource import ReadResource, format_bytes


class Lcd(ReadResource):
    def __init__(self, serial_port, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # By deferring the port assignment until after construction, we prevent the port from
        # opening immediately, so that it can be opened manually
        self._ser = serial.Serial(baudrate=9600,
                                  bytesize=serial.EIGHTBITS,
                                  parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE)
        self._ser.port = serial_port

    @property
    def name(self):
        return 'LCD'

    def _open(self):
        if super()._open():
            self._ser.open()
            return True
        return False

    def _close(self):
        self._ser.close()
        return super()._close()

    def _process_data(self, data):
        self._ser.flush()  # Make sure the buffer is empty before writing more to it
        num_written = self._ser.write(data)

        # Make sure we wrote the expected number of bytes
        if num_written != len(data):
            logger.error(f"Expected to send {len(data)} bytes ({format_bytes(data)}),"
                         f" but only sent {num_written} bytes")
