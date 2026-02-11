"""
fire/addNew.py
- Add new fire extinguisher to table
"""

import csv
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QDialog, QWidget, QFormLayout, QLineEdit, QComboBox, QMessageBox, QDateEdit,
                             QDialogButtonBox, QVBoxLayout, QHBoxLayout, QGroupBox, QScrollArea)

center = QtCore.Qt.AlignmentFlag.AlignCenter
today  = QtCore.QDate.currentDate()
csvFile = "extinguishers.csv"
pdfFile = "extinguishers.pdf"



class AddNew(QDialog):
    def __init__(self, width, labels, makeTable):
        super().__init__(parent=None)

        self.makeTable = makeTable

        self.setWindowTitle("Add New")
        self.setWindowIcon(QtGui.QIcon("./DRDO-logo.png"))

        dialogLayout = QVBoxLayout(self)
        self.setLayout(dialogLayout)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        dialogLayout.addWidget(scroll)

        centralWidget = QWidget(scroll)
        centralLayout = QVBoxLayout(centralWidget)
        scroll.setWidget(centralWidget)

        groupbox = QGroupBox("Enter Fire Extinguisher Details", self)
        groupboxLayout = QFormLayout(groupbox)
        groupboxLayout.setVerticalSpacing(  int(width * 0.02))
        groupboxLayout.setHorizontalSpacing(int(width * 0.04))
        centralLayout.addWidget(groupbox)

        self.exType = QComboBox(groupbox)
        self.exType.setEditable(True)
        self.exType.addItems(["Water", "Foam", "Dry Powder", "CO2", "Clean Agent", "Class D/ TEC/ Pyromet", "Class F", "Other (type here...)"])
        self.exType.currentTextChanged.connect(self.exTypeCondition)

        self.mechanism = QComboBox(groupbox)
        self.mechanism.setEditable(True)
        self.mechanism.addItems(["Stored Pressure", "Cartridge", "Other (type here...)"])

        self.capacity = QWidget(groupbox)
        self.capacityLayout = QHBoxLayout(self.capacity)
        self.capVal   = QLineEdit("1", self.capacity)
        self.capUnit  = QComboBox(self.capacity)
        self.capUnit.setEditable(True)
        self.capUnit.addItems(["kg", "L", "Other (type here...)"])
        self.capacityLayout.addWidget(self.capVal)
        self.capacityLayout.addWidget(self.capUnit)
        self.capacityLayout.addStretch(1)

        self.mfgYear   = QLineEdit("2025" , groupbox)
        self.company   = QLineEdit("Fire" , groupbox)
        self.location  = QLineEdit("India", groupbox)
        self.site      = QLineEdit("Delhi", groupbox)
        self.pressTest = QDateEdit(today  , groupbox)
        self.refilled  = QDateEdit(today  , groupbox)
        self.pressTest  .setDisplayFormat("dd/MM/yyyy")
        self.refilled   .setDisplayFormat("dd/MM/yyyy")

        fields = [self.exType, self.mechanism, self.capacity, self.mfgYear, self.company, self.location, self.site, self.pressTest, self.refilled]

        for i in range(len(fields)):
            groupboxLayout.addRow(labels[i], fields[i])

        self.buttonBox = QDialogButtonBox(centralWidget)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok |
                                          QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.addToTable)
        self.buttonBox.rejected.connect(self.reject)
        centralLayout.addWidget(self.buttonBox)

    #***********************************************************************************************************************

    def exTypeCondition(self):
        self.mechanism.clear()
        self.mechanism.setEditable(True)
        if self.exType.currentText() in ["CO2", "Clean Agent"]:
            self.mechanism.addItems(["Stored Pressure", "Other (type here...)"])
        else:
            self.mechanism.addItems(["Stored Pressure", "Cartridge", "Other (type here...)"])

    #***********************************************************************************************************************

    def addToTable(self):
        with open(csvFile, "r") as f:
            readCSV = list(csv.reader(f))

        if not self.mfgYear.text().isdigit() or len(self.mfgYear.text()) < 4:
            QMessageBox.critical(self, "Error", "Enter only 4 digit year.")
            return

        exType = self.exType.currentText()
        mech = self.mechanism.currentText()

        duePressTest = (self.pressTest.date().addYears(3)
                        if exType in ["Water", "Foam"]
                        else self.pressTest.date().addYears(5))
        
        dueRefill = (self.refilled.date().addYears(5)
                     if exType in ["CO2", "Clean Agent", "Dry Powder", "Class D/ TEC/ Pyromet"]
                        and mech == "Stored Pressure"
                     else self.refilled.date().addYears(3))
        
        dueReplace = (int(self.mfgYear.text()) + 15
                      if exType in ["CO2"]
                      else int(self.mfgYear.text()) + 10)

        data =  [exType, self.mechanism.currentText(), f"{self.capVal.text()} {self.capUnit.currentText()}",
                 self.mfgYear.text(), self.company.text(), self.location.text(), self.site.text(), self.pressTest.text(),
                 self.refilled.text(), duePressTest.toString("dd/MM/yyyy"), dueRefill.toString("dd/MM/yyyy"), f"{dueReplace}"]

        readCSV.append(data)
        readCSV = sorted(readCSV, key=lambda x: x[2])
        self.makeTable(readCSV)

        with open(csvFile, "w", newline="") as f:
            writeCSV = csv.writer(f)
            writeCSV.writerows(readCSV)

        super().accept()
