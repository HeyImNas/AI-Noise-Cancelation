#include <emscripten.h>
#include <emscripten/bind.h>
#include "audio/audio_processor.hpp"

using namespace emscripten;

// Global audio processor instance
std::unique_ptr<ain::AudioProcessor> g_audioProcessor;

// JavaScript callback function type
typedef void (*JSProcessedAudioCallback)(const float* data, size_t length);

// Global JavaScript callback
JSProcessedAudioCallback g_jsCallback = nullptr;

// C++ callback that forwards to JavaScript
void cppProcessedAudioCallback(const float* data, size_t length)
{
    if (g_jsCallback) {
        g_jsCallback(data, length);
    }
}

// Initialize the audio processor
bool initializeAudioProcessor(int sampleRate, int channels, int framesPerBuffer)
{
    g_audioProcessor = std::make_unique<ain::AudioProcessor>();
    return g_audioProcessor->initialize(sampleRate, channels, framesPerBuffer);
}

// Start processing audio
bool startAudioProcessing(const std::string& inputDevice)
{
    if (!g_audioProcessor) {
        return false;
    }
    
    g_audioProcessor->setProcessedAudioCallback(cppProcessedAudioCallback);
    return g_audioProcessor->startProcessing(inputDevice);
}

// Stop processing audio
void stopAudioProcessing()
{
    if (g_audioProcessor) {
        g_audioProcessor->stopProcessing();
    }
}

// Set the JavaScript callback
void setJavaScriptCallback(JSProcessedAudioCallback callback)
{
    g_jsCallback = callback;
}

// Get available audio devices
std::vector<std::string> getAvailableAudioDevices()
{
    if (!g_audioProcessor) {
        return std::vector<std::string>();
    }
    return g_audioProcessor->getAvailableDevices();
}

// Set noise suppression level
void setNoiseSuppressionLevel(float level)
{
    if (g_audioProcessor) {
        g_audioProcessor->setNoiseSuppressionLevel(level);
    }
}

// Set voice suppression level
void setVoiceSuppressionLevel(float level)
{
    if (g_audioProcessor) {
        g_audioProcessor->setVoiceSuppressionLevel(level);
    }
}

// Bind functions to JavaScript
EMSCRIPTEN_BINDINGS(audio_bridge) {
    function("initializeAudioProcessor", &initializeAudioProcessor);
    function("startAudioProcessing", &startAudioProcessing);
    function("stopAudioProcessing", &stopAudioProcessing);
    function("setJavaScriptCallback", &setJavaScriptCallback);
    function("getAvailableAudioDevices", &getAvailableAudioDevices);
    function("setNoiseSuppressionLevel", &setNoiseSuppressionLevel);
    function("setVoiceSuppressionLevel", &setVoiceSuppressionLevel);
} 