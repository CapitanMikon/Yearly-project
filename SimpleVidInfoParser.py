import subprocess as sp
import re


class SimpleVidInfoParser:
    __FFMPEG_path = None

    def __init__(self, ffmpeg_path):
        self.__FFMPEG_path = ffmpeg_path

    def __parse_small_info(self, filepath):
        command = [self.__FFMPEG_path, '-hide_banner',
                   '-i', filepath,
                   '-f', 'null', '-']
        pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.DEVNULL, bufsize=10 ** 5)
        (sp.DEVNULL, err) = pipe.communicate()
        info = err.decode("utf8", errors="ignore")
        pipe.terminate()
        del pipe

        parsed_data = {}
        # print(info)
        for line in info.splitlines()[1:]:
            line = line.lstrip()
            if line.startswith("Stream"):
                try:
                    video_size = re.search(r" (\d+)x(\d+)[,\s]", line)
                    video_fps = re.search(r" (\d+.?\d*) fps", line)
                    if video_size:
                        parsed_data["width"] = int(video_size.groups()[0])
                        parsed_data["height"] = int(video_size.groups()[1])
                    if video_fps:
                        parsed_data["fps"] = float(video_fps.groups()[0])
                except Exception:
                    raise IOError("parsing info exeption!")
            if line.startswith("Duration"):
                try:
                    time_raw = line.split(',')
                    time_raw = time_raw[0].split(':')
                    parsed_data["seconds_and_milliseconds"] = float(time_raw[3])
                    time_raw_last = time_raw[3].split('.')
                    parsed_data["hours"] = int(time_raw[1])
                    parsed_data["minutes"] = int(time_raw[2])
                    parsed_data["seconds"] = int(time_raw_last[0])
                    parsed_data["milliseconds"] = int(time_raw_last[1])
                except Exception:
                    raise IOError("parsing info exeption!")
            #if line.startswith("frame"):
            #    frame_raw = line.split(" ")
            #    frame_raw = re.search("frame=\s*(\d+)", line)
            #    parsed_data["total_frames"] = int(frame_raw.groups()[0])
        return parsed_data

    def get_video_resolution(self, filename):
        return self.__parse_small_info(filename)
