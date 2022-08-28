from iec6205621 import IEC6205621, iecError

api = IEC6205621('/dev/ttyUSB0')
try:
    api.update()
    print("manufacturer: ", api.manufacturer)
    print("model:        ", api.model)
    print("serialnumber: ", api.serial_number)
    print("sw_version:   ", api.firmware_version)
    for sensor_name in api.sensors:
        print("%s: %f %s" % (sensor_name, float(api.sensors[sensor_name]['value']or 0.0), api.sensors[sensor_name]['unit']))
except iecError as e:
    print("Error", e)