#pragma once

#include <windows.h>
#include <mmdeviceapi.h>
#include <audioclient.h>
#include <vector>
#include <memory>
#include "audio_device.hpp"

namespace ain {

class AudioProcessor {
public:
    AudioProcessor();
    ~AudioProcessor();

    bool initialize(const wchar_t* inputDeviceId, const wchar_t* outputDeviceId = nullptr);
    bool start();
    void stop();
    bool isRunning() const;

    // Audio processing methods
    void processAudio(const float* input, float* output, int numFrames);
    void setNoiseSuppressionLevel(float level);
    void setVoiceSuppressionLevel(float level);

private:
    std::unique_ptr<AudioDevice> inputDevice;
    std::unique_ptr<AudioDevice> outputDevice;
    
    bool running;
    float noiseSuppressionLevel;
    float voiceSuppressionLevel;
    
    // Buffer for audio processing
    std::vector<float> inputBuffer;
    std::vector<float> outputBuffer;
    
    // Processing methods
    void applyNoiseSuppression(float* buffer, int numFrames);
    void applyVoiceSuppression(float* buffer, int numFrames);
};

} // namespace ain 