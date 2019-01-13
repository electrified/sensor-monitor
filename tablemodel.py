from PySide2.QtCore import (Qt, QAbstractTableModel, QModelIndex)
from hwmon_interface import Sensor

class TableModel(QAbstractTableModel):

    def __init__(self, sensors=None, parent=None):
        super(TableModel, self).__init__(parent)

        if sensors is None:
            self.sensors = []
        else:
            self.sensors = sensors

    def rowCount(self, index=QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self.sensors)

    def columnCount(self, index=QModelIndex()):
        """ Returns the number of columns the model holds. """
        return 2

    def data(self, index, role=Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not
            returning data, return None (PySide equivalent of QT's
            "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.sensors):
            return None

        if role == Qt.DisplayRole:
            label = self.sensors[index.row()].label
            current_value = self.sensors[index.row()].getDisplayValue()

            if index.column() == 0:
                return label
            elif index.column() == 1:
                return current_value

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Sensor"
            elif section == 1:
                return "Current"

        return None

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        for row in range(rows):
            self.sensors.insert(position + row, Sensor())

        self.endInsertRows()
        return True

    def addSensor(self, sensor):
        self.beginInsertRows(QModelIndex(), 0, 0)

        self.sensors.insert(1, sensor)

        self.endInsertRows()
        return True

    #
    # def removeRows(self, position, rows=1, index=QModelIndex()):
    #     """ Remove a row from the model. """
    #     self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
    #
    #     del self.sensors[position:position+rows]
    #
    #     self.endRemoveRows()
    #     return True
    #
    def setData(self, index, value, role=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given
            index and role.
        """
        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.sensors):
            sensor = self.sensors[index.row()]
            if index.column() == 0:
                sensor.label = value
            elif index.column() == 1:
                sensor.current_value = value
            else:
                return False

            self.dataChanged.emit(index, index, 0)
            return True

        return False

    # def updateSensorValue(self, value):


    #
    # def flags(self, index):
    #     """ Set the item flags at the given index. Seems like we're
    #         implementing this function just to see how it's done, as we
    #         manually adjust each tableView to have NoEditTriggers.
    #     """
    #     if not index.isValid():
    #         return Qt.ItemIsEnabled
    #     return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
    #                         Qt.ItemIsEditable)
