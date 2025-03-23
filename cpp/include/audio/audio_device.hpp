#pragma once

#include <windows.h>
#include <mmdeviceapi.h>
#include <functiondiscoverykeys_devpkey.h>
#include <endpointvolume.h>
#include <audioclient.h>
#include <mmdeviceapi.h>

// Forward declarations of COM interfaces
struct IAudioClient;
struct IAudioRenderClient;
struct IAudioCaptureClient;
struct IMMDevice;

namespace ain {

class AudioDevice {
public:
    AudioDevice();
    ~AudioDevice();

    bool initialize(const wchar_t* deviceId, int sampleRate = 44100, int channels = 1, int framesPerBuffer = 1024);
    
    int getSampleRate() const;
    int getChannels() const;
    int getFramesPerBuffer() const;

private:
    IMMDevice* device;
    IAudioClient* audioClient;
    IAudioRenderClient* renderClient;
    IAudioCaptureClient* captureClient;
    
    int sampleRate;
    int channels;
    int framesPerBuffer;
    
    WAVEFORMATEX* waveFormat;
};

} // namespace ain 