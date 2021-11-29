# Yearly project

Call`process_to_signal(filename) from VideoReader class` in your script to convert desired video file into signal representing its luminance frame by frame in outputted txt file or use included main.py (comment out `run_example()` and uncomment `read_input_file_and_process_files()`) and add video files to be processed into the `input.txt` file. <br><br> File paths can be in either Linux or Windows path format. If its Windows format `read_input_file_and_process_files()` in `main.py` will convert it to Linux format.


# Before **first** use
 - you need to **specify path to ffmpeg.exe**
 - e.g. change `__FFMPEG_path = None` to `__FFMPEG_path = Path("C://path/to/your/ffmpeg.exe")` 
 - path to ffmpeg must be wrapped with **Path()** and in Linux path format (on Windows `C:\\Test\Path\file.exe` -> `C://Test/Path/file.exe`)

## Sample
- `Sample001.mp4` is very short 5 frame video
- Order of frames and its overall rgb value is `rgb(0,0,0), rgb(255,255,255), rgb(254,0,0), rgb(0,254,0), rgb(0,0,254)`
- outputted file `\processed\sample001_luminance.txt` contains luminance of each frame
