# AI Noise Cancellation

A real-time noise suppression application that uses AI and signal processing to remove unwanted background noise from your microphone input.

## Features

- Real-time noise suppression
- Adaptive noise profile learning
- AC and constant background noise removal
- Device selection for input and output
- Volume control
- Simple and intuitive UI

## Future Features

### Audio Processing
- [ ] Echo cancellation
- [ ] Voice enhancement
- [ ] Multiple noise profiles for different environments
- [ ] Deep learning-based noise suppression
- [ ] Automatic gain control
- [ ] Audio equalization
- [ ] Keyboard and mouse click suppression

### Recording & Transcription
- [ ] Audio recording capability
- [ ] Real-time transcription
- [ ] Meeting notes generation
- [ ] Multiple language support
- [ ] Speaker diarization

### User Interface
- [ ] Dark mode support
- [ ] Audio visualization
- [ ] Noise level meter
- [ ] System tray integration
- [ ] Keyboard shortcuts
- [ ] Preset profiles for different environments

### Settings & Configuration
- [ ] Save and load user preferences
- [ ] Custom noise profiles
- [ ] Advanced audio settings
- [ ] Auto-start with system
- [ ] Device hotplugging support

### Integration
- [ ] Plugin support for video conferencing apps
- [ ] Virtual audio device support
- [ ] Cloud sync for settings
- [ ] API for third-party integration

## Requirements

- Python 3.8 or later
- Windows, macOS, or Linux operating system
- Microphone and speakers/headphones

## Installation

### Windows
1. Download or clone this repository
2. Double-click `setup.bat`
3. Wait for the installation to complete
4. Run the application using:
   ```bash
   .venv\Scripts\python main.py
   ```

### macOS/Linux
1. Download or clone this repository
2. Open terminal in the project directory
3. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```
4. Run the setup script:
   ```bash
   ./setup.sh
   ```
5. Run the application:
   ```bash
   source .venv/bin/activate && python main.py
   ```

### Manual Installation
If the automatic setup doesn't work, you can install manually:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

1. Select your input device (microphone)
2. Select your output device (speakers)
3. Adjust the volume as needed
4. Click "Start" to begin noise suppression
5. Toggle "Noise Cancellation" on/off to compare the difference

## Troubleshooting

If you encounter any issues during installation:

1. Make sure Python 3.8 or later is installed and added to PATH
2. Try running the manual installation steps
3. Check that all required dependencies are installed:
   ```bash
   pip list
   ```
4. If you get permission errors on Linux/macOS:
   ```bash
   chmod +x setup.sh
   sudo ./setup.sh
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
