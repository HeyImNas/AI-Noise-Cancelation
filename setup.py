from setuptools import setup, find_packages

setup(
    name="ai_noise_cancellation",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'sounddevice>=0.4.5',
        'PyQt6>=6.4.0',
        'scipy>=1.7.0',
        'soundfile>=0.10.3'
    ],
) 