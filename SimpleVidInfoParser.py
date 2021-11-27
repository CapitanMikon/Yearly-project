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

        res = [0, 0]
        # print(info)
        for line in info.splitlines()[1:]:
            if line.startswith("    Stream"):
                try:
                    video_size = re.search(r" (\d+)x(\d+)[,\s]", line)
                    if video_size:
                        res[0] = video_size.groups()[0]
                        res[1] = video_size.groups()[1]
                except Exception:
                    raise IOError("parsing info exeption!")
        return res

    def get_video_resolution(self, filename):
        return self.__parse_small_info(filename)



