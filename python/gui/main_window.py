from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QComboBox, QPushButton, QLabel, QStatusBar,
                             QHBoxLayout, QSlider, QFrame)
from PyQt6.QtCore import Qt, QTimer, QSettings
from PyQt6.QtGui import QIcon, QFont
from audio.processor import AudioProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Noise Cancellation")
        self.setMinimumSize(400, 500)
        
        # Initialize settings
        self.settings = QSettings('AINoiseCancellation', 'App')
        self.dark_mode = self.settings.value('dark_mode', False, type=bool)
        
        # Initialize audio processor
        self.audio_processor = AudioProcessor()
        self.audio_processor.initialize_model()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)  # Increase spacing between widgets
        
        # Create title section with theme toggle
        title_layout = QHBoxLayout()
        title_label = QLabel("Noise Cancellation")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Add theme toggle button
        self.theme_button = QPushButton()
        self.theme_button.setCheckable(True)
        self.theme_button.setChecked(self.dark_mode)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setMinimumHeight(30)
        self.theme_button.setMaximumWidth(100)
        title_layout.addWidget(self.theme_button)
        layout.addLayout(title_layout)
        
        # Add separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Create device selection section
        device_frame = QFrame()
        device_frame.setFrameShape(QFrame.Shape.StyledPanel)
        device_layout = QVBoxLayout(device_frame)
        
        # Input device (Microphone) selection
        mic_label = QLabel("Microphone")
        mic_label.setFont(QFont("Arial", 12))
        device_layout.addWidget(mic_label)
        
        self.input_device_combo = QComboBox()
        self.input_device_combo.setMinimumHeight(30)
        self.refresh_devices()
        device_layout.addWidget(self.input_device_combo)
        
        # Output device (Speaker) selection
        speaker_label = QLabel("Speaker")
        speaker_label.setFont(QFont("Arial", 12))
        device_layout.addWidget(speaker_label)
        
        self.output_device_combo = QComboBox()
        self.output_device_combo.setMinimumHeight(30)
        self.refresh_output_devices()
        device_layout.addWidget(self.output_device_combo)
        
        layout.addWidget(device_frame)
        
        # Create volume control
        volume_frame = QFrame()
        volume_frame.setFrameShape(QFrame.Shape.StyledPanel)
        volume_layout = QVBoxLayout(volume_frame)
        
        volume_label = QLabel("Volume")
        volume_label.setFont(QFont("Arial", 12))
        volume_layout.addWidget(volume_label)
        
        volume_slider_layout = QHBoxLayout()
        self.volume_label = QLabel(f"{int(self.audio_processor.output_volume * 100)}%")
        volume_slider_layout.addWidget(self.volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(int(self.audio_processor.output_volume * 100))
        self.volume_slider.valueChanged.connect(self.update_volume)
        volume_slider_layout.addWidget(self.volume_slider)
        
        max_volume_label = QLabel("100%")
        volume_slider_layout.addWidget(max_volume_label)
        volume_layout.addLayout(volume_slider_layout)
        
        layout.addWidget(volume_frame)
        
        # Create control buttons frame
        controls_frame = QFrame()
        controls_frame.setFrameShape(QFrame.Shape.StyledPanel)
        controls_layout = QVBoxLayout(controls_frame)
        
        # Start/Stop button
        self.start_button = QPushButton("Start")
        self.start_button.setMinimumHeight(40)
        self.start_button.clicked.connect(self.toggle_processing)
        controls_layout.addWidget(self.start_button)
        
        # Filter toggle button
        self.filter_button = QPushButton("Noise Cancellation: On")
        self.filter_button.setCheckable(True)
        self.filter_button.setChecked(True)
        self.filter_button.setMinimumHeight(40)
        self.filter_button.clicked.connect(self.toggle_filter)
        controls_layout.addWidget(self.filter_button)
        
        # Feedback toggle button
        self.feedback_button = QPushButton("Audio Feedback: On")
        self.feedback_button.setCheckable(True)
        self.feedback_button.setChecked(True)
        self.feedback_button.setMinimumHeight(40)
        self.feedback_button.clicked.connect(self.toggle_feedback)
        controls_layout.addWidget(self.feedback_button)
        
        layout.addWidget(controls_frame)
        
        # Add stretch to push everything up
        layout.addStretch()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Initialize processing state
        self.is_processing = False
        
        # Create timer for status updates
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(100)  # Update every 100ms
        
        # Apply initial theme
        self.update_theme()
        
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop processing if it's running
        if self.is_processing:
            self.audio_processor.stop_processing()
        event.accept()
        
    def update_status(self):
        """Update status bar with current processing state"""
        status = "Processing audio..."
        if not self.audio_processor.filter_enabled:
            status += " (Noise Cancellation Off)"
        if not self.audio_processor.feedback_enabled:
            status += " (Audio Feedback Off)"
        self.status_bar.showMessage(status if self.is_processing else "Ready")
        
    def refresh_devices(self):
        """Refresh the list of available input devices"""
        self.input_device_combo.clear()
        devices = self.audio_processor.get_available_devices()
        for device in devices:
            if device['max_input_channels'] > 0:  # Only show input devices
                self.input_device_combo.addItem(device['name'])
                
    def refresh_output_devices(self):
        """Refresh the list of available output devices"""
        self.output_device_combo.clear()
        devices = self.audio_processor.get_available_devices()
        for device in devices:
            if device['max_output_channels'] > 0:  # Only show output devices
                self.output_device_combo.addItem(device['name'])
                
    def toggle_processing(self):
        """Toggle audio processing on/off"""
        if not self.is_processing:
            # Start processing
            input_device_name = self.input_device_combo.currentText()
            output_device_name = self.output_device_combo.currentText()
            
            if self.audio_processor.set_devices(input_device_name, output_device_name):
                self.audio_processor.is_running = True
                self.audio_processor.start_processing()  # Start processing thread first
                self.audio_processor.start_stream()      # Then start audio stream
                self.start_button.setText("Stop Processing")
                self.is_processing = True
            else:
                self.status_bar.showMessage("Error: Could not set audio devices")
        else:
            # Stop processing
            self.audio_processor.stop_processing()
            self.start_button.setText("Start Processing")
            self.is_processing = False 
        
    def toggle_filter(self):
        """Toggle noise suppression filter on/off"""
        self.audio_processor.filter_enabled = self.filter_button.isChecked()
        self.filter_button.setText(f"Noise Cancellation: {'On' if self.audio_processor.filter_enabled else 'Off'}")
        
    def toggle_feedback(self):
        """Toggle audio feedback on/off"""
        self.audio_processor.feedback_enabled = self.feedback_button.isChecked()
        self.feedback_button.setText(f"Audio Feedback: {'On' if self.audio_processor.feedback_enabled else 'Off'}")
        
    def update_noise_threshold(self, value):
        """Update noise threshold value"""
        self.audio_processor.noise_threshold = value / 1000.0
        self.noise_threshold_label.setText(f"{self.audio_processor.noise_threshold:.3f}")
        
    def update_voice_threshold(self, value):
        """Update voice threshold value"""
        self.audio_processor.voice_threshold = value / 100.0
        self.voice_threshold_label.setText(f"{self.audio_processor.voice_threshold:.3f}")
        
    def update_volume(self, value):
        """Update output volume value"""
        self.audio_processor.output_volume = value / 100.0
        self.volume_label.setText(f"{value}%")
        
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.dark_mode = self.theme_button.isChecked()
        self.settings.setValue('dark_mode', self.dark_mode)
        self.update_theme()
        
    def update_theme(self):
        """Update the application theme"""
        if self.dark_mode:
            self.theme_button.setText("Light Mode")
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QFrame {
                    background-color: #2d2d2d;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton {
                    background-color: #4a5eff;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #2b3cc7;
                }
                QPushButton:hover {
                    background-color: #3a4eef;
                }
                QComboBox {
                    background-color: #3d3d3d;
                    color: white;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: #3d3d3d;
                    color: white;
                    selection-background-color: #4a5eff;
                }
                QLabel {
                    color: #ffffff;
                }
                QSlider::groove:horizontal {
                    border: 1px solid #555555;
                    height: 8px;
                    background: #3d3d3d;
                    margin: 2px 0;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #4a5eff;
                    border: 1px solid #4a5eff;
                    width: 18px;
                    margin: -2px 0;
                    border-radius: 9px;
                }
                QStatusBar {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
            """)
        else:
            self.theme_button.setText("Dark Mode")
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ffffff;
                    color: #000000;
                }
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QFrame {
                    background-color: #f5f5f5;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton {
                    background-color: #4a5eff;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #2b3cc7;
                }
                QPushButton:hover {
                    background-color: #3a4eef;
                }
                QComboBox {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border: none;
                }
                QComboBox QAbstractItemView {
                    selection-background-color: #4a5eff;
                    selection-color: white;
                }
                QSlider::groove:horizontal {
                    border: 1px solid #999999;
                    height: 8px;
                    background: #ffffff;
                    margin: 2px 0;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #4a5eff;
                    border: 1px solid #5c5c5c;
                    width: 18px;
                    margin: -2px 0;
                    border-radius: 9px;
                }
                QStatusBar {
                    background-color: #f5f5f5;
                    color: #000000;
                }
            """) 