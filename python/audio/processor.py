import numpy as np
import sounddevice as sd
import torch
import torchaudio
from typing import Optional, Callable
import queue
import threading
from scipy import signal

class AudioProcessor:
    def __init__(self, 
                 sample_rate: int = 44100,
                 channels: int = 1,
                 chunk_size: int = 1024,
                 input_device: Optional[str] = None,
                 output_device: Optional[str] = None):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.input_device = input_device
        self.output_device = output_device
        self.is_running = False
        self.feedback_enabled = True
        self.filter_enabled = True  # Add filter toggle flag
        self.audio_queue = queue.Queue()
        self.processed_queue = queue.Queue()
        self.stream_thread = None
        self.processing_thread = None
        
        # Initialize output volume parameter (0.0 to 1.0)
        self.output_volume = 1.0  # Default to 100% volume
        
        # Initialize noise suppression parameters with much more aggressive values
        self.noise_threshold = 0.35  # Increased from 0.05 to 0.35 (7x more aggressive)
        self.voice_threshold = 0.25  # Increased from 0.15 to 0.25 (more selective for voice)
        self.smoothing_factor = 0.99  # Increased from 0.98 to 0.99 for more stable noise profile
        self.noise_learning_rate = 0.001
        self.min_noise_floor = 0.0001
        
        # AC-specific parameters with increased suppression
        self.ac_freq_range = (30, 300)  # Widened AC frequency range to catch more noise
        self.ac_bins = None  # Will be initialized in _init_ac_bins
        self.ac_suppression_factor = 0.98  # Increased from 0.95 to 0.98 (much stronger AC suppression)
        
        # Initialize noise profile and statistics
        self.noise_profile = np.zeros(chunk_size // 2 + 1)  # For FFT bins
        self.noise_std = np.zeros(chunk_size // 2 + 1)
        self.signal_energy = 0
        self.noise_energy = 0
        self.learning_noise = True
        self.noise_samples = 0
        self.max_noise_samples = 300  # Increased for better noise learning
        
        # Initialize AC frequency bins
        self._init_ac_bins()
        
    def _init_ac_bins(self):
        """Initialize the frequency bins that correspond to AC noise"""
        freqs = np.fft.rfftfreq(self.chunk_size, 1/self.sample_rate)
        self.ac_bins = np.where((freqs >= self.ac_freq_range[0]) & 
                              (freqs <= self.ac_freq_range[1]))[0]
        
    def initialize_model(self):
        """Initialize the noise suppression model"""
        # For now, we'll use a simple noise suppression approach
        # This will be replaced with a more sophisticated model later
        pass
        
    def start_processing(self):
        """Start the audio processing thread"""
        if self.is_running:
            return
            
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._process_audio)
        self.processing_thread.start()
        
    def stop_processing(self):
        """Stop the audio processing thread"""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join()
        if self.stream_thread:
            self.stream_thread.join()
            
    def _process_audio(self):
        """Main audio processing loop"""
        while self.is_running:
            try:
                # Get audio chunk from queue
                audio_chunk = self.audio_queue.get(timeout=0.1)
                
                # Apply sensitivity adjustment
                audio_chunk = audio_chunk * self.output_volume
                
                # Apply noise suppression if enabled
                if self.filter_enabled:
                    processed_chunk = self._apply_noise_suppression(audio_chunk)
                else:
                    processed_chunk = audio_chunk
                
                # Put processed audio in output queue
                self.processed_queue.put(processed_chunk)
                
            except queue.Empty:
                continue
                
    def _apply_noise_suppression(self, audio_chunk):
        """Apply noise suppression to the audio chunk using spectral gating"""
        # Convert to float32 if needed
        audio = audio_chunk.astype(np.float32)
        
        # Apply window function to reduce spectral leakage
        window = np.hanning(len(audio))
        audio_windowed = audio * window
        
        # Compute FFT
        spec = np.fft.rfft(audio_windowed, axis=0)
        magnitude = np.abs(spec)
        phase = np.angle(spec)
        
        # Calculate signal energy
        current_energy = np.mean(magnitude ** 2)
        
        # Update noise profile during initial learning phase
        if self.learning_noise and self.noise_samples < self.max_noise_samples:
            # Update overall noise profile with more aggressive learning
            self.noise_profile = (self.noise_profile * self.noise_samples + magnitude * 1.5) / (self.noise_samples + 1)
            self.noise_std = np.sqrt((self.noise_std ** 2 * self.noise_samples + (magnitude - self.noise_profile) ** 2) / (self.noise_samples + 1))
            
            # Specifically learn AC noise profile with overestimation
            if self.noise_samples > 50:  # Start learning AC profile after some initial samples
                ac_profile = np.mean(magnitude[self.ac_bins])
                self.noise_profile[self.ac_bins] = np.maximum(
                    self.noise_profile[self.ac_bins],
                    ac_profile * 2.0  # Double the AC noise estimation
                )
            
            self.noise_samples += 1
            if self.noise_samples >= self.max_noise_samples:
                self.learning_noise = False
                print("Noise profile learning completed")
        
        # Calculate noise floor with enhanced AC suppression
        noise_floor = self.noise_profile + self.noise_std * self.noise_threshold
        
        # Apply spectral gating with more aggressive suppression
        # 1. Compute spectral gain with increased threshold
        gain = np.maximum(0, (magnitude - noise_floor * 1.5) / magnitude)
        
        # 2. Apply stronger suppression to AC frequencies
        if not self.learning_noise:
            ac_gain = gain[self.ac_bins] * (1 - self.ac_suppression_factor)
            gain[self.ac_bins] = np.minimum(gain[self.ac_bins], ac_gain)
        
        # 3. Apply voice activity detection with more aggressive threshold
        is_voice = current_energy > self.voice_threshold
        if not is_voice:
            gain *= 0.05  # Reduced from 0.1 to 0.05 for more aggressive noise suppression
        
        # 4. Smooth the gain to avoid musical noise
        gain = signal.medfilt(gain, kernel_size=7)  # Increased kernel size for smoother suppression
        
        # 5. Apply gain to magnitude spectrum
        magnitude = magnitude * gain
        
        # 6. Update noise profile slowly
        if not self.learning_noise:
            # Update overall noise profile more aggressively
            self.noise_profile = (self.smoothing_factor * self.noise_profile + 
                                (1 - self.smoothing_factor) * magnitude * 1.2)
            
            # Update AC noise profile more aggressively
            ac_magnitude = magnitude[self.ac_bins]
            self.noise_profile[self.ac_bins] = np.maximum(
                self.noise_profile[self.ac_bins],
                ac_magnitude * 0.9  # Increased from 0.8 to 0.9 for stronger AC suppression
            )
        
        # Reconstruct signal
        spec = magnitude * np.exp(1j * phase)
        processed = np.fft.irfft(spec, axis=0)
        
        # Apply inverse window
        processed = processed / window
        
        # Normalize
        processed = processed / (np.max(np.abs(processed)) + 1e-6)
        
        return processed
                
    def audio_callback(self, indata, outdata, frames, time, status):
        """Callback for audio stream"""
        if status:
            print(f"Status: {status}")
            
        # Put input audio in processing queue
        self.audio_queue.put(indata.copy())
        
        # Get processed audio from output queue
        try:
            processed_audio = self.processed_queue.get_nowait()
            if self.feedback_enabled:
                # Apply output volume adjustment
                outdata[:] = processed_audio * self.output_volume
            else:
                outdata[:] = np.zeros_like(indata)  # Output silence when feedback is disabled
        except queue.Empty:
            if self.feedback_enabled:
                # Apply output volume adjustment to raw audio as well
                outdata[:] = indata * self.output_volume
            else:
                outdata[:] = np.zeros_like(indata)  # Output silence when feedback is disabled
            
    def _run_stream(self):
        """Run the audio stream in a separate thread"""
        try:
            # Get device info
            input_info = sd.query_devices(self.input_device)
            output_info = sd.query_devices(self.output_device)
            
            # Update channels based on device capabilities
            input_channels = min(self.channels, input_info['max_input_channels'])
            output_channels = min(self.channels, output_info['max_output_channels'])
            
            # Create stream with correct channel configuration
            with sd.Stream(
                device=(self.input_device, self.output_device),
                channels=(input_channels, output_channels),
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                callback=self.audio_callback
            ):
                while self.is_running:
                    sd.sleep(100)
        except Exception as e:
            print(f"Error in audio stream: {e}")
            self.stop_processing()
            
    def start_stream(self):
        """Start the audio stream in a separate thread"""
        self.stream_thread = threading.Thread(target=self._run_stream)
        self.stream_thread.start()
            
    def get_available_devices(self):
        """Get list of available audio devices"""
        return sd.query_devices()
        
    def set_devices(self, input_device_name: str, output_device_name: str):
        """Set both input and output devices"""
        devices = self.get_available_devices()
        
        # Find input device
        input_found = False
        for i, device in enumerate(devices):
            if device['name'] == input_device_name:
                self.input_device = i
                input_found = True
                # Update channels based on input device capabilities
                self.channels = min(self.channels, device['max_input_channels'])
                break
                
        # Find output device
        output_found = False
        for i, device in enumerate(devices):
            if device['name'] == output_device_name:
                self.output_device = i
                output_found = True
                break
                
        return input_found and output_found 