# AI Noise Cancellation

Real-time noise and voice suppression using AI techniques.

## Features

- Real-time audio processing
- Noise suppression
- Voice suppression
- Device selection
- Dark mode support
- Audio visualization
- Volume control
- Feedback control

## Requirements

- Python 3.8+
- PyQt6
- NumPy
- SoundDevice
- PyTorch (for noise suppression)
- CUDA (optional, for GPU acceleration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Noise-Cancelation.git
cd AI-Noise-Cancelation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python python/main.py
```

2. Select your input and output devices from the dropdown menus
3. Click "Start" to begin processing
4. Adjust noise and voice suppression levels as needed
5. Use the volume slider to control output volume
6. Toggle dark mode using the theme button

## Project Structure

```
.
├── python/
│   ├── main.py              # Main application entry point
│   ├── gui/
│   │   ├── main_window.py   # Main window implementation
│   │   └── widgets.py       # Custom widgets
│   └── audio/
│       └── processor.py     # Audio processing implementation
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Future Considerations

- WebAssembly integration for web-based deployment
- Additional noise suppression algorithms
- Real-time audio visualization
- Batch processing mode
- Audio recording and playback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
