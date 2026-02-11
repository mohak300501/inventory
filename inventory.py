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
        self.setWindowIcon(QtGui.QIcon("./DRDO-logo.png"))
        
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
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)
        
        self.setLayout(layout)
    
    def getDate(self):
        return self.dateEdit.date()

class TablePage(QWidget):
    def __init__(self, parent=None, fire_window=None):
        super().__init__(parent)
        self.fire_window = fire_window
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
        
        # Scrollable table area
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        
        self.table = QTableWidget(2, 2, self)
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        
        scrollArea.setWidget(self.table)
        layout.addWidget(scrollArea)
        
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
        """Initialize table with 2 data rows and 2 data columns plus Total row/column"""
        # 2 data rows + 1 total row, 2 data cols + 1 total col
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
        
        # Set first column label for the data row
        self.table.item(1, 0).setText("A")
        self.table.item(1, 1).setText("1")
        
        # Add buttons
        self.addColBtn = QPushButton("Add\nColumn", self)
        self.addColBtn.clicked.connect(self.addColumn)
        self.table.setCellWidget(0, 2, self.addColBtn)
        
        self.addRowBtn = QPushButton("Add\nRow", self)
        self.addRowBtn.clicked.connect(self.addRow)
        self.table.setCellWidget(2, 0, self.addRowBtn)
        
        # Set total labels
        self.updateTotalsLabels()
        
        self.resizeColumns()
        self.resizeRows()
    
    def updateTotalsLabels(self):
        """Update the total row and column labels"""
        totalRow = self.table.rowCount() - 1
        totalCol = self.table.columnCount() - 1
        
        # Total column header
        if self.table.item(0, totalCol):
            self.table.item(0, totalCol).setText("Total")
        
        # Total row header
        if self.table.item(totalRow, 0):
            self.table.item(totalRow, 0).setText("Total")
        
        # Total row, total column intersection
        if self.table.item(totalRow, totalCol):
            self.table.item(totalRow, totalCol).setText("Total")
    
    def addColumn(self):
        """Add a new column before the Total column"""
        currentCols = self.table.columnCount()
        self.table.insertColumn(currentCols - 1)  # Insert before Total
        
        # Initialize new column cells with empty items
        for i in range(self.table.rowCount()):
            item = QTableWidgetItem("")
            self.table.setItem(i, currentCols - 1, item)
        
        # Move Add Column button to the new last data column (row 0)
        self.addColBtn = QPushButton("Add\nColumn", self)
        self.addColBtn.clicked.connect(self.addColumn)
        self.table.setCellWidget(0, currentCols - 1, self.addColBtn)
        
        # Update Total column labels
        self.updateTotalsLabels()
        self.resizeColumns()
    
    def addRow(self):
        """Add a new row before the Total row"""
        currentRows = self.table.rowCount()
        self.table.insertRow(currentRows - 1)  # Insert before Total
        
        # Initialize new row cells with empty items
        for j in range(self.table.columnCount()):
            item = QTableWidgetItem("")
            self.table.setItem(currentRows - 1, j, item)
        
        # Move Add Row button to the new last data row (column 0)
        self.addRowBtn = QPushButton("Add\nRow", self)
        self.addRowBtn.clicked.connect(self.addRow)
        self.table.setCellWidget(currentRows - 1, 0, self.addRowBtn)
        
        # Update Total row labels
        self.updateTotalsLabels()
        self.resizeRows()
    
    def createTotalColumn(self):
        """Create/update the Total column"""
        totalCol = self.table.columnCount() - 1
        if self.table.item(0, totalCol) is None:
            for i in range(self.table.rowCount()):
                item = QTableWidgetItem("")
                self.table.setItem(i, totalCol, item)
        
        # Set header for total column
        self.table.item(0, totalCol).setText("Total")
        # Set label for total row
        self.table.item(self.table.rowCount() - 1, totalCol).setText("Total")
    
    def createTotalRow(self):
        """Create/update the Total row"""
        totalRow = self.table.rowCount() - 1
        if self.table.item(totalRow, 0) is None:
            for j in range(self.table.columnCount()):
                item = QTableWidgetItem("")
                self.table.setItem(totalRow, j, item)
        
        # Set label for total row
        self.table.item(totalRow, 0).setText("Total")
    
    def resizeColumns(self):
        """Resize columns to content"""
        for i in range(self.table.columnCount()):
            self.table.resizeColumnToContents(i)
    
    def resizeRows(self):
        """Resize rows to content"""
        for i in range(self.table.rowCount()):
            self.table.resizeRowToContents(i)
    
    def loadTableFromDate(self, date):
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
            
            # Calculate data dimensions (excluding potential total row/column from CSV)
            # We'll treat the CSV data as-is and add our own total row/column
            num_rows = len(rows)  # All rows from CSV
            num_cols = max(len(row) for row in rows) if rows else 1
            
            # Set table dimensions: CSV rows + 1 total row, CSV cols + 1 total col
            self.table.setRowCount(num_rows + 1)
            self.table.setColumnCount(num_cols + 1)
            
            # Fill data from CSV
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(value)
                    self.table.setItem(i, j, item)
                
                # Fill empty cells in this row
                for j in range(len(row), num_cols + 1):
                    item = QTableWidgetItem("")
                    self.table.setItem(i, j, item)
            
            # Initialize total row with empty cells
            for j in range(num_cols + 1):
                item = QTableWidgetItem("")
                self.table.setItem(num_rows, j, item)
            
            # Add buttons
            self.addColBtn = QPushButton("Add\nColumn", self)
            self.addColBtn.clicked.connect(self.addColumn)
            self.table.setCellWidget(0, num_cols, self.addColBtn)
            
            self.addRowBtn = QPushButton("Add\nRow", self)
            self.addRowBtn.clicked.connect(self.addRow)
            self.table.setCellWidget(num_rows, 0, self.addRowBtn)
            
            # Update total labels
            self.updateTotalsLabels()
            
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
        
        # Extract table data excluding buttons and totals
        rows = []
        totalRow = self.table.rowCount() - 1
        totalCol = self.table.columnCount() - 1
        
        # Extract data rows (excluding total row)
        for i in range(totalRow):
            row = []
            for j in range(totalCol):
                cell_widget = self.table.cellWidget(i, j)
                if cell_widget is not None:
                    # Skip cells with buttons
                    row.append("")
                else:
                    item = self.table.item(i, j)
                    if item:
                        row.append(item.text())
                    else:
                        row.append("")
            rows.append(row)
        
        # Save to CSV
        try:
            with open(csvFilePath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            
            QMessageBox.information(self, "Success", f"Table for {dateStr} saved.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving table: {str(e)}")
    
    def onBack(self):
        """Handle back button with confirmation"""
        reply = QMessageBox.question(self, "Confirmation", "Is all data saved?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.fire_window.gotoMainPage()
    
    def onSavePDF(self):
        """Handle save PDF with confirmation"""
        reply = QMessageBox.question(self, "Confirmation", "Is all data saved?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
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
    def __init__(self, parent=None, fire_window=None):
        super().__init__(parent)
        self.fire_window = fire_window
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
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(slot)
            return btn
        
        addBtn = make_btn("Add New Table", fire_window.addNewTable)
        viewBtn = make_btn("View Table", fire_window.viewTable)
        
        grid.addWidget(addBtn, 0, 0)
        grid.addWidget(viewBtn, 0, 1)
        
        grid.setRowStretch(0, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        
        btnWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        logo.setPixmap(QtGui.QPixmap("./DRDO-logo.png"))
        logo.setScaledContents(True)
        logo.setFixedWidth(int(width * 0.13))
        logo.setFixedHeight(int(width * 0.13))
        layout.addWidget(logo, alignment=center)
        layout.addStretch(1)
        
        self.setLayout(layout)

class Fire(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Inventory Management")
        self.setWindowIcon(QtGui.QIcon("./DRDO-logo.png"))
        
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        
        self.mainPage = MainPage(self, self)
        self.tablePage = TablePage(self, self)
        
        self.stack.addWidget(self.mainPage)
        self.stack.addWidget(self.tablePage)
        
        self.stack.setCurrentWidget(self.mainPage)
        self.showMainPage()
    
    def showMainPage(self):
        self.stack.setCurrentWidget(self.mainPage)
        self.mainPage.left_pane.setVisible(True)
    
    def gotoMainPage(self):
        self.showMainPage()
    
    def addNewTable(self):
        """Add a new table for selected date"""
        dlg = DateSelector(self)
        if dlg.exec() == QDialog.Accepted:
            selectedDate = dlg.getDate()
            dateStr = selectedDate.toString("dd-MM-yyyy")
            csvFilePath = os.path.join("CSV", f"{dateStr}.csv")
            
            # Create CSV folder if it doesn't exist
            os.makedirs("CSV", exist_ok=True)
            
            # Create new CSV file with default data
            try:
                with open(csvFilePath, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Site/Item", "I"])
                    writer.writerow(["A", "1"])
                
                # Load the table
                self.tablePage.loadTableFromDate(selectedDate)
                self.stack.setCurrentWidget(self.tablePage)
                self.mainPage.left_pane.setVisible(False)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error creating table: {str(e)}")
    
    def viewTable(self):
        """View table for selected date"""
        dlg = DateSelector(self)
        if dlg.exec() == QDialog.Accepted:
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

window = Fire()
window.showMaximized()

app.exec()
