import sys
import fitz  # PyMuPDF
import os
import tempfile
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QFileDialog, QLabel,
                            QScrollArea, QToolBar, QStatusBar, QDialog,
                            QListWidget, QListWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QAction, QIcon

class AttachmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Good PDF - Attachments")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Create list widget for attachments
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        
        # Create buttons
        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_selected)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_selected)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        
    def set_attachments(self, attachments):
        self.attachments = attachments
        self.list_widget.clear()
        
        if not attachments:
            self.list_widget.addItem("No attachments found")
            self.save_button.setEnabled(False)
            self.open_button.setEnabled(False)
        else:
            for name, data in attachments:
                size = len(data)
                size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                self.list_widget.addItem(f"{name} ({size_str})")
            self.save_button.setEnabled(True)
            self.open_button.setEnabled(True)
    
    def get_selected_attachment(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Good PDF", "Please select an attachment")
            return None, None
            
        selected_name = current_item.text().split(" (")[0]  # Remove size information
        for name, data in self.attachments:
            if name == selected_name:
                return name, data
        return None, None
    
    def open_selected(self):
        name, data = self.get_selected_attachment()
        if not data:
            return
            
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(name)[1]) as temp_file:
                temp_file.write(data)
                temp_path = temp_file.name
            
            # Open the file with the system's default application
            if sys.platform == 'win32':
                os.startfile(temp_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', temp_path])
            else:  # Linux
                subprocess.run(['xdg-open', temp_path])
                
        except Exception as e:
            QMessageBox.critical(self, "Good PDF", f"Failed to open attachment: {str(e)}")
    
    def save_selected(self):
        name, data = self.get_selected_attachment()
        if not data:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Good PDF - Save Attachment", name
        )
        if file_name:
            try:
                with open(file_name, 'wb') as f:
                    f.write(data)
                QMessageBox.information(self, "Good PDF", "Attachment saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Good PDF", f"Failed to save attachment: {str(e)}")

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Good PDF")
        self.setMinimumSize(800, 600)
        
        # Initialize variables
        self.current_document = None
        self.current_page = 0
        self.total_pages = 0
        self.attachments = []
        self.zoom_level = 2.0  # Initial zoom level
        self.display_mode = "normal"  # normal, fill, or fit
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create scroll area for PDF display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)
        
        # Create label for displaying PDF pages
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.page_label)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Create navigation buttons
        self.create_navigation_buttons()
        
        # Create attachment dialog
        self.attachment_dialog = AttachmentDialog(self)
        
    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Open file action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        # Show attachments action
        self.attachment_action = QAction("Attachments", self)
        self.attachment_action.triggered.connect(self.show_attachments)
        self.attachment_action.setEnabled(False)
        toolbar.addAction(self.attachment_action)
        
    def create_navigation_buttons(self):
        nav_layout = QHBoxLayout()
        
        # Add stretchable space on the left
        nav_layout.addStretch()
        
        # Fill button
        fill_button = QPushButton("Fill")
        fill_button.setFixedWidth(40)
        fill_button.clicked.connect(self.fill_page)
        nav_layout.addWidget(fill_button)
        
        # Zoom out button
        zoom_out_button = QPushButton("-")
        zoom_out_button.setFixedWidth(30)
        zoom_out_button.clicked.connect(self.zoom_out)
        nav_layout.addWidget(zoom_out_button)
        
        prev_button = QPushButton("Previous")
        prev_button.clicked.connect(self.previous_page)
        nav_layout.addWidget(prev_button)
        
        self.page_info = QLabel("Page 0 of 0")
        nav_layout.addWidget(self.page_info)
        
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_page)
        nav_layout.addWidget(next_button)
        
        # Zoom in button
        zoom_in_button = QPushButton("+")
        zoom_in_button.setFixedWidth(30)
        zoom_in_button.clicked.connect(self.zoom_in)
        nav_layout.addWidget(zoom_in_button)
        
        # Fit button
        fit_button = QPushButton("Fit")
        fit_button.setFixedWidth(40)
        fit_button.clicked.connect(self.fit_page)
        nav_layout.addWidget(fit_button)
        
        # Add stretchable space on the right
        nav_layout.addStretch()
        
        self.layout.addLayout(nav_layout)
        
    def fill_page(self):
        if not self.current_document:
            return
            
        # Calculate zoom level to fill width
        page = self.current_document[self.current_page]
        page_width = page.rect.width
        view_width = self.scroll_area.viewport().width()
        self.zoom_level = view_width / page_width
        self.display_mode = "fill"
        self.display_page()
        self.status_bar.showMessage(f"Fill width (Zoom: {self.zoom_level:.1f}x)")
    
    def fit_page(self):
        if not self.current_document:
            return
            
        # Calculate zoom level to fit page
        page = self.current_document[self.current_page]
        page_width = page.rect.width
        page_height = page.rect.height
        view_width = self.scroll_area.viewport().width()
        view_height = self.scroll_area.viewport().height()
        
        # Calculate zoom to fit both width and height
        width_ratio = view_width / page_width
        height_ratio = view_height / page_height
        self.zoom_level = min(width_ratio, height_ratio)
        self.display_mode = "fit"
        self.display_page()
        self.status_bar.showMessage(f"Fit page (Zoom: {self.zoom_level:.1f}x)")
    
    def zoom_in(self):
        self.display_mode = "normal"
        self.zoom_level = min(self.zoom_level + 0.5, 5.0)  # Maximum zoom level of 5x
        self.display_page()
        self.status_bar.showMessage(f"Zoom: {self.zoom_level:.1f}x")
    
    def zoom_out(self):
        self.display_mode = "normal"
        self.zoom_level = max(self.zoom_level - 0.5, 0.5)  # Minimum zoom level of 0.5x
        self.display_page()
        self.status_bar.showMessage(f"Zoom: {self.zoom_level:.1f}x")
    
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Good PDF - Open File", "", "PDF Files (*.pdf)"
        )
        
        if file_name:
            try:
                self.current_document = fitz.open(file_name)
                self.total_pages = len(self.current_document)
                self.current_page = 0
                
                self.attachments = []
                seen_attachments = set()
                
                try:
                    for name in self.current_document.embfile_names():
                        try:
                            file_data = self.current_document.embfile_get(name)
                            if isinstance(file_data, bytes):
                                if name not in seen_attachments:
                                    self.attachments.append((name, file_data))
                                    seen_attachments.add(name)
                            else:
                                file_data = file_data.read()
                                if name not in seen_attachments:
                                    self.attachments.append((name, file_data))
                                    seen_attachments.add(name)
                        except Exception as e:
                            pass
                except Exception as e:
                    pass
                
                for i in range(len(self.current_document)):
                    page = self.current_document[i]
                    for annot in page.annots():
                        if annot.type[0] == 17:
                            try:
                                file_name = annot.info.get("filename", "unnamed")
                                file_data = annot.get_file()
                                if file_data:
                                    is_duplicate = False
                                    for existing_name, existing_data in self.attachments:
                                        if len(file_data) == len(existing_data) and file_data[:100] == existing_data[:100]:
                                            is_duplicate = True
                                            break
                                    
                                    if not is_duplicate and file_name not in seen_attachments:
                                        self.attachments.append((file_name, file_data))
                                        seen_attachments.add(file_name)
                            except Exception as e:
                                pass
                
                self.attachments.sort(key=lambda x: x[0].lower())
                
                if self.attachments:
                    self.status_bar.showMessage(f"Found {len(self.attachments)} attachments")
                else:
                    self.status_bar.showMessage("No attachments found")
                
                self.attachment_action.setEnabled(len(self.attachments) > 0)
                
                self.display_page()
            except Exception as e:
                self.status_bar.showMessage(f"Error opening file: {str(e)}")
    
    def show_attachments(self):
        if not self.attachments:
            QMessageBox.information(self, "Good PDF", "This PDF does not contain any attachments.")
            return
        self.attachment_dialog.set_attachments(self.attachments)
        self.attachment_dialog.exec()
    
    def display_page(self):
        if not self.current_document:
            return
            
        page = self.current_document[self.current_page]
        pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom_level, self.zoom_level))
        
        # Convert to QImage
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        
        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(img)
        self.page_label.setPixmap(pixmap)
        
        # Update page info
        self.page_info.setText(f"Page {self.current_page + 1} of {self.total_pages}")
        
    def next_page(self):
        if self.current_document and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_page()
            
    def previous_page(self):
        if self.current_document and self.current_page > 0:
            self.current_page -= 1
            self.display_page()
            
    def closeEvent(self, event):
        if self.current_document:
            self.current_document.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 