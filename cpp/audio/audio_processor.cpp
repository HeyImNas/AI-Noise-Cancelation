#include "audio/audio_processor.hpp"
#include <algorithm>
#include <cmath>
#include <iostream>

namespace ain {

AudioProcessor::AudioProcessor()
    : running(false)
    , noiseSuppressionLevel(0.5f)
    , voiceSuppressionLevel(0.5f)
{
}

AudioProcessor::~AudioProcessor()
{
    stop();
}

bool AudioProcessor::initialize(const wchar_t* inputDeviceId, const wchar_t* outputDeviceId)
{
    inputDevice = std::make_unique<AudioDevice>();
    if (!inputDevice->initialize(inputDeviceId)) {
        std::cerr << "Failed to initialize input device" << std::endl;
        return false;
    }

    if (outputDeviceId) {
        outputDevice = std::make_unique<AudioDevice>();
        if (!outputDevice->initialize(outputDeviceId)) {
            std::cerr << "Failed to initialize output device" << std::endl;
            return false;
        }
    }

    // Initialize buffers
    int bufferSize = inputDevice->getFramesPerBuffer() * inputDevice->getChannels();
    inputBuffer.resize(bufferSize);
    outputBuffer.resize(bufferSize);

    return true;
}

bool AudioProcessor::start()
{
    if (running) {
        return true;
    }

    running = true;
    return true;
}

void AudioProcessor::stop()
{
    running = false;
}

bool AudioProcessor::isRunning() const
{
    return running;
}

void AudioProcessor::processAudio(const float* input, float* output, int numFrames)
{
    if (!running) {
        return;
    }

    // Copy input to processing buffer
    std::copy(input, input + numFrames * inputDevice->getChannels(), inputBuffer.begin());

    // Apply noise suppression
    applyNoiseSuppression(inputBuffer.data(), numFrames);

    // Apply voice suppression
    applyVoiceSuppression(inputBuffer.data(), numFrames);

    // Copy processed audio to output
    std::copy(inputBuffer.begin(), inputBuffer.begin() + numFrames * inputDevice->getChannels(), output);
}

void AudioProcessor::setNoiseSuppressionLevel(float level)
{
    noiseSuppressionLevel = std::clamp(level, 0.0f, 1.0f);
}

void AudioProcessor::setVoiceSuppressionLevel(float level)
{
    voiceSuppressionLevel = std::clamp(level, 0.0f, 1.0f);
}

void AudioProcessor::applyNoiseSuppression(float* buffer, int numFrames)
{
    // TODO: Implement noise suppression algorithm
    // This is a placeholder that just reduces the amplitude based on the suppression level
    for (int i = 0; i < numFrames * inputDevice->getChannels(); ++i) {
        float magnitude = std::abs(buffer[i]);
        if (magnitude < noiseSuppressionLevel) {
            buffer[i] *= 0.1f;
        }
    }
}

void AudioProcessor::applyVoiceSuppression(float* buffer, int numFrames)
{
    // TODO: Implement voice suppression algorithm
    // This is a placeholder that just reduces the amplitude based on the suppression level
    for (int i = 0; i < numFrames * inputDevice->getChannels(); ++i) {
        float magnitude = std::abs(buffer[i]);
        if (magnitude > voiceSuppressionLevel) {
            buffer[i] *= 0.5f;
        }
    }
}

} // namespace ain 