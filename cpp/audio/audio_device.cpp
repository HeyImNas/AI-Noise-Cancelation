#include "audio/audio_device.hpp"
#include <stdexcept>

namespace ain {

AudioDevice::AudioDevice()
    : device(nullptr)
    , audioClient(nullptr)
    , renderClient(nullptr)
    , captureClient(nullptr)
    , sampleRate(44100)
    , channels(1)
    , framesPerBuffer(1024)
    , waveFormat(nullptr)
{
}

AudioDevice::~AudioDevice()
{
    if (waveFormat) {
        CoTaskMemFree(waveFormat);
    }
    if (captureClient) {
        captureClient->Release();
    }
    if (renderClient) {
        renderClient->Release();
    }
    if (audioClient) {
        audioClient->Release();
    }
    if (device) {
        device->Release();
    }
}

bool AudioDevice::initialize(const wchar_t* deviceId, int sampleRate, int channels, int framesPerBuffer)
{
    this->sampleRate = sampleRate;
    this->channels = channels;
    this->framesPerBuffer = framesPerBuffer;

    HRESULT hr = CoInitializeEx(nullptr, COINIT_MULTITHREADED);
    if (FAILED(hr)) {
        return false;
    }

    IMMDeviceEnumerator* deviceEnumerator = nullptr;
    hr = CoCreateInstance(
        __uuidof(MMDeviceEnumerator), nullptr, CLSCTX_ALL,
        __uuidof(IMMDeviceEnumerator), (void**)&deviceEnumerator
    );
    if (FAILED(hr)) {
        CoUninitialize();
        return false;
    }

    hr = deviceEnumerator->GetDevice(deviceId, &device);
    deviceEnumerator->Release();
    if (FAILED(hr)) {
        CoUninitialize();
        return false;
    }

    hr = device->Activate(__uuidof(IAudioClient), CLSCTX_ALL, nullptr, (void**)&audioClient);
    if (FAILED(hr)) {
        return false;
    }

    hr = audioClient->GetMixFormat(&waveFormat);
    if (FAILED(hr)) {
        return false;
    }

    hr = audioClient->Initialize(
        AUDCLNT_SHAREMODE_SHARED,
        0,
        10000000, // 1 second buffer
        0,
        waveFormat,
        nullptr
    );
    if (FAILED(hr)) {
        return false;
    }

    hr = audioClient->GetService(
        __uuidof(IAudioRenderClient),
        (void**)&renderClient
    );
    if (FAILED(hr)) {
        return false;
    }

    hr = audioClient->GetService(
        __uuidof(IAudioCaptureClient),
        (void**)&captureClient
    );
    if (FAILED(hr)) {
        return false;
    }

    return true;
}

int AudioDevice::getSampleRate() const
{
    return sampleRate;
}

int AudioDevice::getChannels() const
{
    return channels;
}

int AudioDevice::getFramesPerBuffer() const
{
    return framesPerBuffer;
}

} // namespace ain 