# SurveillanceVideo Documentation

## Overview
The `SurveillanceVideo.py` script is designed to manage and process surveillance video feeds. It encompasses functionalities such as capturing video, processing frames, and detecting motion.

## Features
- **Real-time video capture:** The script can capture video from connected cameras or video files.
- **Motion detection:** Incorporates algorithms for detecting motion within the video stream.
- **Frame processing:** Allows for frame extraction and processing for analysis.

## Installation
To set up the project, you need Python 3.6 or higher. You can install the necessary dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage
Run the script using the command line. Specify the source of the video:

```bash
python SurveillanceVideo.py --source <video_source>
```

### Command Line Options
- `--source`: Specifies the video source (e.g., camera index, video file path).
- `--output`: (Optional) Save processed output to the specified directory.

## Important Classes and Functions
### `SurveillanceVideo`
- **Methods:**
  - `__init__(self, source)`: Initializes the video capture.
  - `start_capture(self)`: Begins capturing video.
  - `detect_motion(self)`: Implements motion detection logic.

## Conclusion
This documentation provides an overview of the `SurveillanceVideo.py` script. For further details, refer to the code comments and structure within the repository.