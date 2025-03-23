cmake_minimum_required(VERSION 3.10)
project(AINoiseCancellation)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(OpenMP REQUIRED)

# Add source files
set(SOURCES
    audio/audio_processor.cpp
    audio/audio_device.cpp
)

# Create shared library
add_library(ainoisecancellation SHARED ${SOURCES})

# Include directories
target_include_directories(ainoisecancellation PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Link libraries
target_link_libraries(ainoisecancellation
    PRIVATE
    OpenMP::OpenMP_CXX
    ole32
    oleaut32
    avrt
)

# Installation
install(TARGETS ainoisecancellation
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
) 