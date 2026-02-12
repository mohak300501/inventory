"""
inventory/inventory.py
- Inventory Management Software
"""

import sys, csv, os
from pathlib import Path
from savePDF import savePDF
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QMessageBox, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QStackedWidget, 
                             QSizePolicy, QGridLayout, QDialog, QDateEdit, QDialogButtonBox, QFrame, QScrollArea)

center = QtCore.Qt.AlignmentFlag.AlignCenter
today  = lambda: QtCore.QDate.currentDate()
appcon = "./DRDO-logo.png"




class HeadBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        titleLabel = QLabel("INVENTORY MANAGEMENT SOFTWARE", self)
        titleLabel.setAlignment(center)
        titleLabel.setObjectName("title")
        layout.addWidget(titleLabel, alignment=center)
        self.setLayout(layout)

class DateSelector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setWindowIcon(QtGui.QIcon(appcon))

        layout = QVBoxLayout(self)

        # Date label
        label = QLabel("Select Date:", self)
        layout.addWidget(label)

        # Date edit
        self.dateEdit = QDateEdit(today(), self)
        self.dateEdit.setDisplayFormat("dd/MM/yyyy")
        self.dateEdit.setCalendarPopup(True)
        layout.addWidget(self.dateEdit)

        # Buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def getDate(self):
        return self.dateEdit.date()

class TablePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentDate = None
        self.csvFolder = "CSV"

        layout = QVBoxLayout(self)

        # Head bar
        layout.addWidget(HeadBar(self))

        # Date subtitle
        self.dateLabel = QLabel("", self)
        self.dateLabel.setAlignment(center)
        self.dateLabel.setObjectName("dateSubtitle")
        layout.addWidget(self.dateLabel)

        # Add Column/Row buttons layout (above table)
        topBtnLayout = QHBoxLayout()
        topBtnLayout.addStretch(1)

        self.addColBtn = QPushButton("Add\nColumn", self)
        self.addColBtn.setObjectName("bluBtn")
        self.addColBtn.setMinimumHeight(int(height * 0.04))
        self.addColBtn.setMinimumWidth(int(width * 0.08))
        self.addColBtn.setFont(QtGui.QFont("", int(width * 0.009)))
        self.addColBtn.clicked.connect(self.addColumn)
        topBtnLayout.addWidget(self.addColBtn)

        self.addRowBtn = QPushButton("Add\nRow", self)
        self.addRowBtn.setObjectName("bluBtn")
        self.addRowBtn.setMinimumHeight(int(height * 0.04))
        self.addRowBtn.setMinimumWidth(int(width * 0.08))
        self.addRowBtn.setFont(QtGui.QFont("", int(width * 0.009)))
        self.addRowBtn.clicked.connect(self.addRow)
        topBtnLayout.addWidget(self.addRowBtn)

        topBtnLayout.addStretch(1)
        layout.addLayout(topBtnLayout)

        # Scrollable table area
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)

        self.table = QTableWidget(3, 3, self)
        self.table.setEditTriggers(QTableWidget.EditTrigger.AnyKeyPressed)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        scrollArea.setWidget(self.table)
        layout.addWidget(scrollArea, stretch=1)

        # Bottom button layout
        btnLayout = QHBoxLayout()
        btnLayout.addStretch(1)

        self.saveTableBtn = QPushButton("Save Table", self)
        self.saveTableBtn.setObjectName("bluBtn")
        self.saveTableBtn.setMinimumHeight(int(height * 0.05))
        self.saveTableBtn.setFont(QtGui.QFont("", int(width * 0.011)))
        self.saveTableBtn.clicked.connect(self.saveTable)
        btnLayout.addWidget(self.saveTableBtn)

        backBtn = QPushButton("Back", self)
        backBtn.setObjectName("bluBtn")
        backBtn.setMinimumHeight(int(height * 0.05))
        backBtn.setFont(QtGui.QFont("", int(width * 0.011)))
        backBtn.clicked.connect(self.onBack)
        btnLayout.addWidget(backBtn)

        self.savePdfBtn = QPushButton("Save PDF", self)
        self.savePdfBtn.setObjectName("bluBtn")
        self.savePdfBtn.setMinimumHeight(int(height * 0.05))
        self.savePdfBtn.setFont(QtGui.QFont("", int(width * 0.011)))
        self.savePdfBtn.clicked.connect(self.onSavePDF)
        btnLayout.addWidget(self.savePdfBtn)

        btnLayout.addStretch(1)

        layout.addLayout(btnLayout)

        # Initialize table with sample data
        self.initializeTable()

    def initializeTable(self):
        """Initialize table with 3x3 default grid"""
        self.table.setRowCount(3)
        self.table.setColumnCount(3)

        # Initialize cells with empty content
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = QTableWidgetItem("")
                self.table.setItem(i, j, item)

        # Set headers for the first row
        self.table.item(0, 0).setText("Site/Item")
        self.table.item(0, 1).setText("I")
        self.table.item(0, 2).setText("Total")

        # Set first column label for the data rows
        self.table.item(1, 0).setText("A")
        self.table.item(2, 0).setText("Total")

        # Set data cells
        self.table.item(1, 1).setText("1")
        self.table.item(1, 2).setText("1")
        self.table.item(2, 1).setText("1")
        self.table.item(2, 2).setText("1")

        self.resizeColumns()
        self.resizeRows()

    def addColumn(self):
        """Add a new column before the Total column"""
        currentCols = self.table.columnCount()
        self.table.insertColumn(currentCols - 1)  # Insert before Total

        # Initialize new column cells with empty items
        for i in range(self.table.rowCount()):
            item = QTableWidgetItem("")
            self.table.setItem(i, currentCols - 1, item)

        # Update Total column label to new position
        totalCol = self.table.columnCount() - 1
        self.table.item(0, totalCol).setText("Total")
        if self.table.rowCount() > 0:
            self.table.item(self.table.rowCount() - 1, totalCol).setText("Total")

        self.resizeColumns()

    def addRow(self):
        """Add a new row before the Total row"""
        currentRows = self.table.rowCount()
        self.table.insertRow(currentRows - 1)  # Insert before Total

        # Initialize new row cells with empty items
        for j in range(self.table.columnCount()):
            item = QTableWidgetItem("")
            self.table.setItem(currentRows - 1, j, item)

        # Update Total row label to new position
        totalRow = self.table.rowCount() - 1
        self.table.item(totalRow, 0).setText("Total")

        self.resizeRows()

    def resizeColumns(self):
        """Resize columns to content"""
        for i in range(self.table.columnCount()):
            self.table.resizeColumnToContents(i)

    def resizeRows(self):
        """Resize rows to content"""
        for i in range(self.table.rowCount()):
            self.table.resizeRowToContents(i)

    def loadTableFromDate(self, date: QtCore.QDate):
        """Load table data from CSV file for given date"""
        self.currentDate = date
        dateStr = date.toString("dd-MM-yyyy")
        self.dateLabel.setText(dateStr)

        csvFilePath = os.path.join(self.csvFolder, f"{dateStr}.csv")

        if not os.path.exists(csvFilePath):
            self.initializeTable()
            return

        try:
            with open(csvFilePath, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)

            if not rows:
                self.initializeTable()
                return

            # Calculate data dimensions
            num_rows = len(rows)
            num_cols = max(len(row) for row in rows) if rows else 1

            # Set table dimensions
            self.table.setRowCount(num_rows)
            self.table.setColumnCount(num_cols)

            # Fill data from CSV
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(value)
                    self.table.setItem(i, j, item)

                # Fill empty cells in this row
                for j in range(len(row), num_cols):
                    item = QTableWidgetItem("")
                    self.table.setItem(i, j, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading table: {str(e)}")
            self.initializeTable()

        self.resizeColumns()
        self.resizeRows()

    def saveTable(self):
        """Save table to CSV file with calculated totals"""
        if not self.currentDate:
            QMessageBox.warning(self, "Error", "No date selected")
            return

        dateStr = self.currentDate.toString("dd-MM-yyyy")
        csvFilePath = os.path.join(self.csvFolder, f"{dateStr}.csv")

        # Create CSV folder if it doesn't exist
        os.makedirs(self.csvFolder, exist_ok=True)

        try:
            # Extract table data
            rows = []
            totalRow = self.table.rowCount() - 1
            totalCol = self.table.columnCount() - 1

            # Extract data rows and columns
            for i in range(self.table.rowCount()):
                row = []
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j)
                    if item:
                        row.append(item.text())
                    else:
                        row.append("")
                rows.append(row)

            # Calculate totals for each column (excluding Total row and column)
            for j in range(1, totalCol):  # Skip first column (headers)
                total = 0
                for i in range(1, totalRow):  # Skip first row (headers)
                    cell_text = rows[i][j]
                    try:
                        total += float(cell_text) if cell_text else 0
                    except ValueError:
                        total += 0
                rows[totalRow][j] = str(total)

            # Calculate totals for each row (excluding Total row and column)
            for i in range(1, totalRow):  # Skip first row (headers)
                total = 0
                for j in range(1, totalCol):  # Skip first column (headers)
                    cell_text = rows[i][j]
                    try:
                        total += float(cell_text) if cell_text else 0
                    except ValueError:
                        total += 0
                rows[i][totalCol] = str(total)

            # Calculate grand total (sum of all data cells)
            grand_total = 0
            for i in range(1, totalRow):
                for j in range(1, totalCol):
                    cell_text = rows[i][j]
                    try:
                        grand_total += float(cell_text) if cell_text else 0
                    except ValueError:
                        grand_total += 0
            rows[totalRow][totalCol] = str(grand_total)

            # Save to CSV
            with open(csvFilePath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            # Load updated data in table
            self.loadTableFromDate(self.currentDate)

            QMessageBox.information(self, "Success", f"Table for {dateStr} saved.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving table: {str(e)}")

    def onBack(self):
        """Handle back button with confirmation"""
        reply = QMessageBox.question(self, "Confirmation", "Is all data saved?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.parent().parent().showMainPage()

    def onSavePDF(self):
        """Handle save PDF with confirmation"""
        reply = QMessageBox.question(self, "Confirmation", "Is all data saved?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if not self.currentDate:
                QMessageBox.warning(self, "Error", "No date selected")
                return

            dateStr = self.currentDate.toString("dd-MM-yyyy")
            csvFilePath = os.path.join(self.csvFolder, f"{dateStr}.csv")
            pdfFilePath = os.path.join("PDF", f"{dateStr}.pdf")

            os.makedirs("PDF", exist_ok=True)

            try:
                savePDF(csvFilePath, pdfFilePath)
                QMessageBox.information(self, "Success", f"PDF saved successfully for {dateStr}!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving PDF: {str(e)}")

class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)

        # Left pane
        self.left_pane = LeftPane(self)
        main_layout.addWidget(self.left_pane)

        # Right pane
        right_widget = QWidget(self)
        right_layout = QVBoxLayout(right_widget)

        # Title
        titleLabel = QLabel("INVENTORY MANAGEMENT SOFTWARE", right_widget)
        titleLabel.setAlignment(center)
        titleLabel.setObjectName("title")
        right_layout.addWidget(titleLabel)

        # Dashboard label
        dash_label = QLabel("Dashboard", right_widget)
        dash_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        dash_label.setObjectName("dashboardLabel")
        right_layout.addWidget(dash_label)

        # Buttons
        btnWidget = QWidget(right_widget)
        grid = QGridLayout(btnWidget)
        grid.setSpacing(int(height * 0.03))
        button_size = int(height * 0.09)
        font = QtGui.QFont()
        font.setPointSize(int(width * 0.014))

        def make_btn(text, slot):
            btn = QPushButton(text, btnWidget)
            btn.setObjectName("bluBtn")
            btn.setMinimumHeight(button_size)
            btn.setFont(font)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.clicked.connect(slot)
            return btn

        addBtn = make_btn("Add New Table", self.parent().addNewTable)
        viewBtn = make_btn("View Table", self.parent().viewTable)

        grid.addWidget(addBtn, 0, 0)
        grid.addWidget(viewBtn, 0, 1)

        grid.setRowStretch(0, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        btnWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_layout.addWidget(btnWidget, stretch=1)
        right_layout.addStretch(1)

        main_layout.addWidget(right_widget)
        self.setLayout(main_layout)

class LeftPane(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("leftPane")
        layout = QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Logo
        logo = QLabel(self)
        logo.setPixmap(QtGui.QPixmap(appcon))
        logo.setScaledContents(True)
        logo.setFixedWidth(int(width * 0.13))
        logo.setFixedHeight(int(width * 0.13))
        layout.addWidget(logo, alignment=center)
        layout.addStretch(1)

        self.setLayout(layout)

class Inventory(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Inventory Management")
        self.setWindowIcon(QtGui.QIcon(appcon))

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.mainPage = MainPage(self)
        self.tablePage = TablePage(self)

        self.stack.addWidget(self.mainPage)
        self.stack.addWidget(self.tablePage)

        self.stack.setCurrentWidget(self.mainPage)
        self.showMainPage()

    def showMainPage(self):
        self.stack.setCurrentWidget(self.mainPage)
        self.mainPage.left_pane.setVisible(True)

    def addNewTable(self):
        """Add a new table for selected date"""
        dlg = DateSelector(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            selectedDate = dlg.getDate()
            dateStr = selectedDate.toString("dd-MM-yyyy")
            csvFilePath = os.path.join("CSV", f"{dateStr}.csv")

            # Create CSV folder if it doesn't exist
            os.makedirs("CSV", exist_ok=True)

            # Check if file already exists
            if os.path.exists(csvFilePath):
                QMessageBox.warning(self, "Alert", f"Table for {dateStr} already exists")
                return

            # Create new CSV file with default data
            try:
                with open(csvFilePath, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Site/Item", "I", "Total"])
                    writer.writerow(["A", "1", "1"])
                    writer.writerow(["Total", "1", "1"])

                # Load the table
                self.tablePage.loadTableFromDate(selectedDate)
                self.stack.setCurrentWidget(self.tablePage)
                self.mainPage.left_pane.setVisible(False)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error creating table: {str(e)}")

    def viewTable(self):
        """View table for selected date"""
        dlg = DateSelector(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            selectedDate = dlg.getDate()
            dateStr = selectedDate.toString("dd-MM-yyyy")
            csvFilePath = os.path.join("CSV", f"{dateStr}.csv")

            if not os.path.exists(csvFilePath):
                QMessageBox.warning(self, "Error", f"No table found for {dateStr}")
                return

            # Load the table
            self.tablePage.loadTableFromDate(selectedDate)
            self.stack.setCurrentWidget(self.tablePage)
            self.mainPage.left_pane.setVisible(False)




app = QApplication(sys.argv)

screenSize = app.primaryScreen().size()
width, height = screenSize.width(), screenSize.height()

fontSizes = (int(width * 0.01), int(width * 0.02), int(width * 0.016))
styleSheet = Path("./style.qss").read_text()
app.setStyleSheet(styleSheet % fontSizes)

window = Inventory()
window.showMaximized()

app.exec()
