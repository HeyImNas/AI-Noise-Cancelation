cmake_minimum_required(VERSION 3.10)
project(AI_Noise_Cancelation)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add source files
add_library(audio_processor
    cpp/audio/audio_processor.cpp
)

# Add include directories
target_include_directories(audio_processor
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/cpp/include
)

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Add compiler warnings
if(MSVC)
    target_compile_options(audio_processor PRIVATE /W4)
else()
    target_compile_options(audio_processor PRIVATE -Wall -Wextra -Wpedantic)
endif() 