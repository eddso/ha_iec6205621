"""Support for IEC 62056-21 Smart Meter."""
# sources
# https://github.com/lvzon/dsmr-p1-parser/blob/master/doc/IEC-62056-21-notes.md
# https://onemeter.com/docs/device/obis/

import serial
import time
import re
import logging

class iecError(Exception):
    pass

class IEC6205621:
    def __init__(self, port, logger=None):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 300
        self.ser.bytesize = 7
        self.ser.parity = 'E'
        self.ser.stopbits = 1
        self.ser.timeout = 7
        self.retry = 2

        self.serial_number = None
        self.manufacturer = None
        self.model = None
        self.firmware_version = None
        self.sensors = {
            "energy_consumption_total": {"name":"Energy Consumption Total","value":None,"unit":"kWh"},
            "energy_feed_total": {"name":"Energy Feed Total","value":None,"unit":"kWh"},
        }

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
        
    def update(self):
        count=0
        while True:
            count+=1
            try:
                self.ser.baudrate = 300
                if not self.ser.is_open:
                    self.ser.open()
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
    
                self.send(b'/?!\r\n')
                data = self.read(b'\n')
                if data:
                    self.model = data.lstrip('/')
                    self.send(b'\x060\x350\r\n')
                    time.sleep(0.5)
                    self.ser.baudrate = 9600
                    data = self.read(b'\x03')
                    self.parse_obis(data)
                self.ser.close()
                return
            except (serial.SerialException, OSError, ValueError, Exception) as exception:
                self.ser.close()
                self.logger.error(exception)
                if count >= self.retry:
                    raise iecError(exception)
                pass
                time.sleep(1)

    def read(self, end):
        data = self.ser.read_until(end)
        if data:
            self.logger.debug("< %s", data)
            data = data.decode("utf-8").rstrip()
            return data
        raise ValueError("Read timeout")

    def send(self, data):
        self.logger.debug("> %s", data)
        self.ser.write(data)
        self.ser.flush()

    def parse_obis(self, data):
        if data:
            data = data.split('\r\n')
            for i in data:
                if '1.8.0' in i:
                    self.sensors["energy_consumption_total"]['value'] = float(re.search("\((.*?)\)", i).group(1))
                elif '2.8.0' in i:
                    self.sensors["energy_feed_total"]['value'] = float(re.search("\((.*?)\)", i).group(1))
                elif '0.0.0' in i:
                    self.serial_number = re.search("\((.*?)\)", i).group(1)
                elif '0.0.1' in i:
                    self.manufacturer = re.search("\((.*?)\)", i).group(1)
                elif '0.2.0' in i:
                    self.firmware_version = re.search("\((.*?)\)", i).group(1)




