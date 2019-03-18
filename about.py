from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton)

class About(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("About")
        self.aboutLabel = QLabel("Asus sensor monitor v1")

        self.okButton = QPushButton("OK!")

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.aboutLabel)
        self.mainLayout.addWidget(self.okButton)