from math import ceil
import SimpleVidInfoParser
import subprocess as sp
import numpy as np
from os import mkdir, path
from pathlib import Path
import sys
import datetime


class VideoReader:
    __FFMPEG_path = None

    def __init__(self, write_warns_errors):
        self.__write_warns_errors = write_warns_errors
        if self.__write_warns_errors:
            print("\n\t[warns and errors will be written to \"warnings_errors.txt\"]\n")
        self.__file_path = None
        self.__command = None
        self.__pipe = None
        self.__video_width = None
        self.__video_height = None
        self.__counter = None
        self.__video_fps = None
        self.__file = None
        self.__video_total_frames = None
        self.__simple_vid_parser = SimpleVidInfoParser.SimpleVidInfoParser(self.__FFMPEG_path)

    def __process_frame(self):
        n_bytes = 3 * self.__video_width * self.__video_height
        try:
            read_bytes = self.__pipe.stdout.read(n_bytes)
            if len(read_bytes) == 0:
                self.__file.close()
                return False
            assert len(read_bytes) == n_bytes
            result = np.fromstring(read_bytes, dtype='uint8')
            r = 0
            g = 0
            b = 0
            factor = float(self.__video_height * self.__video_width)
            rgb = np.array(result).reshape(self.__video_height, self.__video_width, 3)
            r, g, b = rgb[:, :, 0].sum() / factor, rgb[:, :, 1].sum() / factor, rgb[:, :, 2].sum() / factor

            self.__file.write("%s\n" % ("{:.10f}".format(self.__calculate_luminance(r, g, b))))
            print("\r%s Processed frame %s/%s!" % (datetime.datetime.now().strftime("[%H:%M:%S %d-%m-%Y]"), self.__counter, self.__video_total_frames), end="")
            self.__counter += 1
            return True
        except IOError:
            print("An error occurred!")
            sys.exit(-1)
        finally:
            self.__pipe.stdout.flush()

    def __calculate_luminance(self, r, g, b):
        r_constant = 0.299
        g_constant = 0.587
        b_constant = 0.114
        luminance = (r_constant * r + g_constant * g + b_constant * b)
        luminance /= 255
        return luminance

    def process_to_signal(self, filename):
        if self.__FFMPEG_path is None:
            print("FFMPEG path not specified!")
            sys.exit(-1)
        resolution = self.__parse_little_info(filename)
        self.__initialize_processing(filename, resolution)
        print("%s Processing file [%s] (%sx%s) %s fps" % (datetime.datetime.now().strftime("[%H:%M:%S %d-%m-%Y]"), self.__file_path.name, self.__video_width, self.__video_height, "{:.2f}".format(self.__video_fps)))
        while True:
            if not self.__process_frame():
                break
        print("\n%s Successfully processed file [%s] (%sx%s) %s fps\n" % (datetime.datetime.now().strftime("[%H:%M:%S %d-%m-%Y]"), self.__file_path.name, self.__video_width, self.__video_height, "{:.2f}".format(self.__video_fps)))
        self.__finish_and_reset()

    def __parse_little_info(self, filename):
        return self.__simple_vid_parser.get_video_resolution(filename)

    def __initialize_processing(self, filename, resolution):
        self.__file_path = Path(filename)
        self.__command = [self.__FFMPEG_path,
                          '-i', self.__file_path,
                          '-f', 'image2pipe',
                          '-pix_fmt', 'rgb24',
                          '-vcodec', 'rawvideo', '-']
        if self.__write_warns_errors:
            self.__errors_file = open("warnings_errors.txt", "a")
            self.__pipe = sp.Popen(self.__command, stdout=sp.PIPE, stderr=self.__errors_file, bufsize=10 ** 8)
        else:
            self.__pipe = sp.Popen(self.__command, stdout=sp.PIPE, stderr=sp.DEVNULL, bufsize=10 ** 8)
        self.__video_width = resolution.get("width")
        self.__video_height = resolution.get("height")
        self.__video_fps = resolution.get("fps")
        self.__video_total_frames = self.__calc_total_frames(resolution)
        self.__counter = 1

        if not path.exists(Path("processed/")):
            mkdir("processed")

        self.__file = open(Path("processed/%s_luminance.txt" % self.__file_path.stem), "w")

    def __finish_and_reset(self):
        self.__file.close()
        if self.__write_warns_errors:
            self.__errors_file.close()
        self.__file_path = None
        self.__command = None
        self.__pipe = None
        self.__video_width = None
        self.__video_height = None
        self.__counter = None
        self.__video_total_frames = None
        self.__file = None
        self.__video_fps = None

    def __duration_to_seconds(self, duration):
        seconds = 0
        seconds += duration["seconds_and_milliseconds"]
        seconds += duration["minutes"]*60
        seconds += duration["hours"]*60*60
        return seconds

    def __calc_total_frames(self, parsed_data):
        frames = 0
        frames += self.__duration_to_seconds(parsed_data) * ceil(parsed_data.get("fps"))
        return int(frames)

