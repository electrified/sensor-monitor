# find hwmon interface that is asus sensors
from re import findall
from operator import attrgetter


class Sensor():
    def __init__(self, name, label=None, current_value=0):
        self.label = label
        self.name = name
        self.type = ''.join(filter(lambda x: x.isalpha(), name))
        self.id = findall(r"\d+", name)[0]
        self.current_value = current_value

    def setLabel(self, label):
        self.label = label

    def setCurrentValue(self, value):
        self.current_value = int(value)

    def getScaledValue(self):
        return {
            'in': lambda x: x / 1000,
            'temp': lambda x: x / 1000,
            'fan': lambda x: x,
            'curr': lambda x: x / 1000,
        }[self.type](self.current_value)

    def getUnits(self):
        return {
            'in': 'V',
            'temp': 'C',
            'fan': 'RPM',
            'curr': 'A'
        }[self.type]

    def getDisplayValue(self):
        return "{} {}".format(self.getScaledValue(), self.getUnits())


def get_list_of_sensors():
    import os

    files = []
    with os.scandir("/sys/class/hwmon/hwmon0/") as it:
        for entry in it:
            if entry.name.endswith('_input') and entry.is_file():
                sensor = Sensor(entry.name.split('_')[0])
                sensor.setLabel(get_sensor_label(sensor.name))
                files.append(sensor)
    files = sorted(files, key=attrgetter("name", "id"))
    return files


def get_sensor_value(sensor):
    with open('/sys/class/hwmon/hwmon0/{sensor}_input'.format(sensor=sensor), 'r') as myfile:
        data = myfile.read().strip()
    return data


def get_sensor_label(sensor):
    with open('/sys/class/hwmon/hwmon0/{sensor}_label'.format(sensor=sensor), 'r') as myfile:
        data = myfile.read().strip()
    return data
