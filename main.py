from sys import exit, argv
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QTableView,
                               QAbstractItemView, QHeaderView)
from PySide2.QtCore import Slot, Qt, QModelIndex, QTimer
# from PySide2.QtWidgets import (QWidget)


from hwmon_interface import get_sensor_value, get_sensor_label, get_list_of_sensors

from tablemodel import TableModel

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.tableModel = TableModel()

        self.tableView = QTableView()
        self.tableView.setModel(self.tableModel)
        # self.tableView.setSortingEnabled(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().hide()
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # self.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableView)
        self.setLayout(self.layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update_sensors_values)
        timer.setInterval(1000)
        timer.start()

        self.get_sensors()


    @Slot()
    def magic(self):
        self.update_sensors_values()

    @Slot()
    def get_sensors(self):
        sensors = get_list_of_sensors()

        for sensor in sensors:
            self.tableModel.addSensor(sensor)
        #
        # for sensor in sensors:
        #     # Step 1: create the  row
        #     self.tableModel.insertRows(0)
        #
        #     # Step 2: get the index of the newly created row and use it.
        #     # to set the name
        #     ix = self.tableModel.index(0, 0, QModelIndex())
        #     self.tableModel.setData(ix, sensor.label, Qt.EditRole)
        #
        #     # Step 3: lather, rinse, repeat for the address.
        #     ix = self.tableModel.index(0, 1, QModelIndex())
        #     self.tableModel.setData(ix, sensor.current_value, Qt.EditRole)

    def update_sensors_values(self):
        for index, sensor in enumerate(self.tableModel.sensors):
            new_value = get_sensor_value(sensor.name)
            sensor.setCurrentValue(new_value)
            self.tableModel.dataChanged.emit(index, index, 0)

if __name__ == "__main__":
    app = QApplication(argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    widget.setWindowTitle("Sensor monitoring")

    exit(app.exec_())