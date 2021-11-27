import VideoReader
from pathlib import Path
from sys import exit
from os import path


def run_example():
    reader = VideoReader.VideoReader(False)
    filepath = Path("sample/sample001.mp4")
    reader.process_to_signal(filepath)


def read_input_file_and_process_files():
    if not path.isfile("input.txt"):
        print("input file not found!")
        exit(-1)
    files_to_process = []
    file = open("input.txt", "r")
    for line in file.read().splitlines():
        if not len(line) == 0:
            files_to_process.append(line.replace("\\", "/"))
    file.close()
    if len(files_to_process) == 0:
        print("input file contains no filepath")
        exit(0)
    reader = VideoReader.VideoReader(False)
    for video_file in files_to_process:
        if path.exists(video_file):
            reader.process_to_signal(video_file)


if __name__ == '__main__':
    run_example()
    # read_input_file_and_process_files()
