"""
inventory/savePDF.py
- Export inventory table data to PDF file
"""

import csv
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox


def savePDF(csvFile, pdfFile):
    """
    Save inventory table from CSV to PDF with multi-page support.
    
    Args:
        csvFile: Path to the CSV file
        pdfFile: Path to the output PDF file
    """
    try:
        with open(csvFile, "r") as f:
            readCSV = list(csv.reader(f))
        
        if not readCSV:
            QMessageBox.warning(None, "Error", "CSV file is empty!")
            return
        
        pdf_writer = QtGui.QPdfWriter(pdfFile)
        pdf_writer.setPageSize(QtGui.QPdfWriter.PageSize.A4)
        pdf_writer.setResolution(300)
        
        # Set landscape orientation for better table display
        try:
            pdf_writer.setPageOrientation(QtGui.QPageLayout.Orientation.Landscape)
        except Exception:
            # fallback for older PyQt5
            pdf_writer.setPageSizeMM(QtCore.QSizeF(297, 210))
        
        painter = QtGui.QPainter(pdf_writer)
        
        # Set up fonts
        header_font = QtGui.QFont("Times New Roman", 11)
        header_font.setBold(True)
        content_font = QtGui.QFont("Times New Roman", 10)
        
        painter.setFont(content_font)
        
        # Set dimensions
        margin = 20
        page_width = pdf_writer.width()
        page_height = pdf_writer.height()
        available_width = page_width - (2 * margin)
        available_height = page_height - (2 * margin)
        
        # Calculate column widths
        num_cols = max(len(row) for row in readCSV) if readCSV else 1
        col_width = available_width / num_cols
        
        # Calculate row height
        metrics = QtGui.QFontMetrics(content_font)
        row_height = metrics.height() + 50
        
        x = margin
        y = margin
        current_row = 0
        
        # Draw each row
        while current_row < len(readCSV):
            row = readCSV[current_row]
            
            # Check if we need a new page
            if y + row_height > available_height:
                pdf_writer.newPage()
                y = margin
            
            # Draw each cell in the row
            for col_idx in range(num_cols):
                cell_text = row[col_idx] if col_idx < len(row) else ""
                cell_rect = QtCore.QRectF(x + (col_idx * col_width), y, col_width, row_height)
                
                # Draw cell border
                painter.drawRect(cell_rect)
                
                # Draw cell text
                text_rect = cell_rect.adjusted(4, 2, -4, -2)
                
                # Use bold font for header row
                if current_row == 0 or (len(readCSV) > 1 and current_row == len(readCSV) - 1):
                    painter.setFont(header_font)
                else:
                    painter.setFont(content_font)
                
                painter.drawText(text_rect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, cell_text)
                painter.setFont(content_font)
            
            y += row_height
            current_row += 1
        
        painter.end()
        # QMessageBox.information(None, "Success", "Your PDF file is saved successfully!")
        
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error saving PDF: {str(e)}")
