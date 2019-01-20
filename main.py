from sys import exit, argv
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QTableView,
                               QAbstractItemView, QHeaderView, QMenuBar, QMenu, QDockWidget)
from PySide2.QtCore import Slot, Qt, QModelIndex, QTimer
from PySide2.QtCharts import QtCharts
from time import time

# from PySide2.QtWidgets import (QWidget)


from hwmon_interface import get_sensor_value, get_sensor_label, get_list_of_sensors

from tablemodel import TableModel

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.sensortypes = ["in", "curr", "fan", "temp"]
        self.chartView = {}

        self.createMenu()
        self.tableModel = TableModel()

        self.dock = QDockWidget()

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

        self.dock.layout().addWidget(self.tableView)

        self.layout = QVBoxLayout()
        self.layout.setMenuBar(self.menuBar)
        self.layout.addWidget(self.dock)
        self.setLayout(self.layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update_sensors_values)
        timer.setInterval(1000)
        timer.start()

        for sensorType in self.sensortypes:
            series = QtCharts.QLineSeries()
            series.append(0, 6)
            series.append(2, 4)

            chart_view = QtCharts.QChartView()
            self.layout.addWidget(chart_view)

            chart_view.chart().addSeries(series)

            chart_view.chart().createDefaultAxes()
            chart_view.chart().legend().setAlignment(Qt.AlignLeft)
            chart_view.chart().axisX().setRange(0, 1000)
            chart_view.chart().axisY().setRange(0, 100)
            chart_view.show()

            self.chartView[sensorType] = chart_view

        self.chartSeries = {}

        self.get_sensors()

        self.updateNumber = 0

    @Slot()
    def magic(self):
        self.update_sensors_values()

    @Slot()
    def get_sensors(self):
        sensors = get_list_of_sensors()

        for sensor in sensors:
            self.tableModel.addSensor(sensor)
            series = QtCharts.QLineSeries()
            series.setName(sensor.label)
            self.chartSeries[sensor.name] = series
            self.chartView[sensor.type].chart().addSeries(series)
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
            sensor.setCurrentValue(get_sensor_value(sensor.name))
            self.tableModel.dataChanged.emit(index, index, 0)
            self.chartView[sensor.type].chart().series()[index].append(self.updateNumber, sensor.getScaledValue())

        self.updateNumber += 1

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.close)


if __name__ == "__main__":
    app = QApplication(argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    widget.setWindowTitle("Sensor monitoring")

    exit(app.exec_())