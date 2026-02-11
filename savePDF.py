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
        font = QtGui.QFont("Times New Roman", 10)
        painter.setFont(font)
        
        # Set dimensions
        margin = 20
        x = margin
        y = margin
        row_height = 40
        
        # Calculate column widths based on number of columns
        num_cols = len(readCSV[0]) if readCSV else 1
        available_width = pdf_writer.width() - (2 * margin)
        col_width = available_width / num_cols
        
        page_height = pdf_writer.height() - (2 * margin)
        
        # Draw each row
        for row_idx, row in enumerate(readCSV):
            # Compute max height for the current row based on text wrapping
            max_row_height = row_height
            cell_texts = []
            
            for cell_idx, cell in enumerate(row):
                text = str(cell)
                rect = QtCore.QRectF(x + (cell_idx * col_width), y, col_width, 1000)
                bounding_rect = painter.boundingRect(rect, QtCore.Qt.TextFlag.TextWordWrap, text)
                max_row_height = max(max_row_height, bounding_rect.height() + 10)
                cell_texts.append(text)
            
            # Check if we need a new page
            if y + max_row_height > page_height:
                pdf_writer.newPage()
                y = margin
            
            # Draw each cell
            for col_idx, text in enumerate(cell_texts):
                cell_rect = QtCore.QRectF(x + (col_idx * col_width), y, col_width, max_row_height)
                painter.drawRect(cell_rect)
                painter.drawText(cell_rect, QtCore.Qt.TextFlag.TextWordWrap | QtCore.Qt.AlignmentFlag.AlignCenter, text)
            
            y += max_row_height
        
        painter.end()
        QMessageBox.information(None, "Success", "Your PDF file is saved successfully!")
        
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error saving PDF: {str(e)}")
