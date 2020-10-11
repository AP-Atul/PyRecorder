"""
File to store all the constants. This file act as a config file
changes made would be applied directly. Make sure everything is correct
"""
# video size, not greater than the original desktop your are working on
VIDEO_SIZE = "1366x768"

# frame rate; fps for the video
FPS = "30"

# codec to render the video
VIDEO_CODEC = "libx264rgb"

# format for video
VIDEO_FORMAT = "x11grab"

# codec to render the audio
AUDIO_CODEC = "aac"

# audio device to listen to
AUDIO_DEVICE = "pulse"

# format for audio
AUDIO_FORMAT = "alsa"
