#!/usr/bin/env python3
import os
import sys
import time
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QFileDialog, QProgressBar, QRadioButton, QButtonGroup,
                             QGroupBox, QSplitter, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from compressor import Compressor

class WorkerSignals(QObject):
    """Defines signals available for the worker thread"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    update_status = pyqtSignal(str)
    update_stats = pyqtSignal(str)

class CompressionWorker(threading.Thread):
    """Worker thread for compression/decompression operations"""
    
    def __init__(self, operation, input_file, output_file, algorithm=None):
        super().__init__()
        self.operation = operation
        self.input_file = input_file
        self.output_file = output_file
        self.algorithm = algorithm
        self.signals = WorkerSignals()
        
    def run(self):
        try:
            compressor = Compressor(self.algorithm) if self.algorithm else Compressor()
            
            if self.operation == "compress":
                self.signals.update_status.emit(f"Compressing {os.path.basename(self.input_file)}...")
                size, ratio, time_taken = compressor.compress_file(self.input_file, self.output_file)
                stats = f"Original size: {os.path.getsize(self.input_file)} bytes\n"
                stats += f"Compressed size: {size} bytes\n"
                stats += f"Compression ratio: {ratio:.2f}%\n"
                stats += f"Time taken: {time_taken:.2f} seconds"
                self.signals.update_stats.emit(stats)
                self.signals.update_status.emit(f"File compressed successfully: {os.path.basename(self.output_file)}")
                
            elif self.operation == "decompress":
                self.signals.update_status.emit(f"Decompressing {os.path.basename(self.input_file)}...")
                size, time_taken = compressor.decompress_file(self.input_file, self.output_file)
                stats = f"Compressed size: {os.path.getsize(self.input_file)} bytes\n"
                stats += f"Decompressed size: {size} bytes\n"
                stats += f"Time taken: {time_taken:.2f} seconds"
                self.signals.update_stats.emit(stats)
                self.signals.update_status.emit(f"File decompressed successfully: {os.path.basename(self.output_file)}")
                
            self.signals.finished.emit()
            
        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.finished.emit()

class FileCompressionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Compression Tool")
        self.setMinimumSize(700, 500)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Operation selection
        operation_group = QGroupBox("Operation")
        operation_layout = QHBoxLayout()
        
        self.compress_radio = QRadioButton("Compress")
        self.decompress_radio = QRadioButton("Decompress")
        self.compress_radio.setChecked(True)
        
        operation_button_group = QButtonGroup(self)
        operation_button_group.addButton(self.compress_radio)
        operation_button_group.addButton(self.decompress_radio)
        
        operation_layout.addWidget(self.compress_radio)
        operation_layout.addWidget(self.decompress_radio)
        operation_group.setLayout(operation_layout)
        
        # Connect signals
        self.compress_radio.toggled.connect(self.update_ui_for_operation)
        
        # Algorithm selection
        algorithm_group = QGroupBox("Compression Algorithm")
        algorithm_layout = QHBoxLayout()
        
        algorithm_label = QLabel("Algorithm:")
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["LZW", "Huffman", "RLE"])
        
        algorithm_layout.addWidget(algorithm_label)
        algorithm_layout.addWidget(self.algorithm_combo)
        algorithm_group.setLayout(algorithm_layout)
        
        # File selection
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        
        input_layout = QHBoxLayout()
        self.input_label = QLabel("Input File:")
        self.input_path = QLabel("No file selected")
        self.input_browse = QPushButton("Browse")
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_path, 1)  # Stretch factor 1
        input_layout.addWidget(self.input_browse)
        
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Output File:")
        self.output_path = QLabel("No file selected")
        self.output_browse = QPushButton("Browse")
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path, 1)  # Stretch factor 1
        output_layout.addWidget(self.output_browse)
        
        file_layout.addLayout(input_layout)
        file_layout.addLayout(output_layout)
        file_group.setLayout(file_layout)
        
        # Connect browse buttons
        self.input_browse.clicked.connect(self.browse_input_file)
        self.output_browse.clicked.connect(self.browse_output_file)
        
        # Status and progress
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        status_group.setLayout(status_layout)
        
        # Process button
        self.process_button = QPushButton("Process")
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_file)
        
        # Statistics area
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        
        stats_layout.addWidget(self.stats_text)
        stats_group.setLayout(stats_layout)
        
        # Add all widgets to main layout
        main_layout.addWidget(operation_group)
        main_layout.addWidget(algorithm_group)
        main_layout.addWidget(file_group)
        main_layout.addWidget(status_group)
        main_layout.addWidget(self.process_button)
        main_layout.addWidget(stats_group)
        
        # Initialize instance variables
        self.input_file = None
        self.output_file = None
        self.worker = None
        self.update_ui_for_operation()
    
    def update_ui_for_operation(self):
        """Update UI elements based on selected operation"""
        is_compress = self.compress_radio.isChecked()
        
        # Update algorithm group visibility
        self.algorithm_combo.setEnabled(is_compress)
        
        # Update input file label
        if is_compress:
            self.input_label.setText("File to Compress:")
            self.output_label.setText("Save Compressed File As:")
        else:
            self.input_label.setText("File to Decompress:")
            self.output_label.setText("Save Decompressed File As:")
        
        # Reset file paths
        self.input_path.setText("No file selected")
        self.output_path.setText("No file selected")
        self.input_file = None
        self.output_file = None
        self.process_button.setEnabled(False)
    
    def browse_input_file(self):
        """Open file dialog to select input file"""
        is_compress = self.compress_radio.isChecked()
        
        if is_compress:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select File to Compress", "", "All Files (*.*)"
            )
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select File to Decompress", "", "Compressed Files (*.cmp);;All Files (*.*)"
            )
        
        if file_path:
            self.input_file = file_path
            self.input_path.setText(os.path.basename(file_path))
            
            # Suggest default output file
            if is_compress:
                self.output_file = file_path + ".cmp"
                self.output_path.setText(os.path.basename(self.output_file))
            else:
                # For decompression, we'll auto-detect from the file
                base_name = os.path.splitext(file_path)[0]
                self.output_file = base_name
                self.output_path.setText(os.path.basename(self.output_file) + " (auto-detect)")
            
            self.update_process_button()
    
    def browse_output_file(self):
        """Open file dialog to select output file"""
        is_compress = self.compress_radio.isChecked()
        
        if is_compress:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Compressed File As", "", "Compressed Files (*.cmp);;All Files (*.*)"
            )
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Decompressed File As", "", "All Files (*.*)"
            )
        
        if file_path:
            self.output_file = file_path
            self.output_path.setText(os.path.basename(file_path))
            self.update_process_button()
    
    def update_process_button(self):
        """Enable or disable process button based on file selection"""
        self.process_button.setEnabled(self.input_file is not None)
    
    def process_file(self):
        """Process the file (compress or decompress)"""
        is_compress = self.compress_radio.isChecked()
        
        if not self.input_file:
            return
        
        # Disable UI during processing
        self.process_button.setEnabled(False)
        self.compress_radio.setEnabled(False)
        self.decompress_radio.setEnabled(False)
        self.algorithm_combo.setEnabled(False)
        self.input_browse.setEnabled(False)
        self.output_browse.setEnabled(False)
        
        # Reset progress and stats
        self.progress_bar.setValue(0)
        
        # Create and start worker thread
        operation = "compress" if is_compress else "decompress"
        algorithm = self.algorithm_combo.currentText().lower() if is_compress else None
        
        self.worker = CompressionWorker(operation, self.input_file, self.output_file, algorithm)
        
        # Connect signals
        self.worker.signals.update_status.connect(self.update_status)
        self.worker.signals.update_stats.connect(self.update_stats)
        self.worker.signals.error.connect(self.handle_error)
        self.worker.signals.finished.connect(self.process_finished)
        
        # Start worker
        self.worker.start()
    
    def update_status(self, status):
        """Update status label"""
        self.status_label.setText(status)
    
    def update_stats(self, stats):
        """Update statistics text area"""
        self.stats_text.setText(stats)
    
    def handle_error(self, error_message):
        """Handle errors during processing"""
        QMessageBox.critical(self, "Error", error_message)
        self.status_label.setText(f"Error: {error_message}")
    
    def process_finished(self):
        """Called when processing is finished"""
        # Re-enable UI
        self.process_button.setEnabled(True)
        self.compress_radio.setEnabled(True)
        self.decompress_radio.setEnabled(True)
        self.algorithm_combo.setEnabled(self.compress_radio.isChecked())
        self.input_browse.setEnabled(True)
        self.output_browse.setEnabled(True)
        self.progress_bar.setValue(100)

def main():
    app = QApplication(sys.argv)
    window = FileCompressionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 