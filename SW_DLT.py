# SW-DLT script, do not copy without permission!

import urllib.parse
import subprocess
import mimetypes
import datetime
import shutil
import sys
import re
import os

try:
    import requests
    import youtube_dl
except:
    pass


class SWDLT:
    FFMPEG_URL = "https://github.com/holzschu/a-Shell-commands/releases/download/0.1/ffmpeg.wasm"
    FFPROBE_URL = "https://github.com/holzschu/a-Shell-commands/releases/download/0.1/ffprobe.wasm"
    REBOOT_EXC = "open shortcuts://run-shortcut?name=SW-DLT&input=text&text=EXCEPTION.vars.restartRequired"
    ERASED_EXC = "open shortcuts://run-shortcut?name=SW-DLT&input=text&text=EXCEPTION.vars.erasedAll"
    DERROR_EXC = "open shortcuts://run-shortcut?name=SW-DLT&input=text&text=EXCEPTION.vars.downloadError"

    def __init__(self, media_url):
        self.media_url = media_url
        self.out_name = datetime.datetime.today().strftime("%d-%m-%y-%H-%M-%S")

    def check_setup(self):
        reboot = False

        if "Package(s) not found" in subprocess.getoutput("pip show youtube-dl"):
            subprocess.run("pip -q install --upgrade youtube-dl")
            reboot = True
        if "Package(s) not found" in subprocess.getoutput("pip show gallery-dl"):
            subprocess.run("pip -q install --upgrade gallery-dl")
            reboot = True
        if reboot is True:
            raise Exception(self.REBOOT_EXC)
        subprocess.run("cd")

        if os.path.exists("./bin") is False:
            subprocess.run("mkdir bin")
            subprocess.run("cd bin")
            req1 = requests.get(self.FFMPEG_URL)
            with open('./ffmpeg.wasm', 'wb') as ffmpeg:
                ffmpeg.write(req1.content)
            ffmpeg.close()

            req2 = requests.get(self.FFPROBE_URL)
            with open('./ffprobe.wasm', 'wb') as ffprobe:
                ffprobe.write(req2.content)
            ffprobe.close()
        else:
            subprocess.run("cd bin")
            if os.path.exists("./ffprobe.wasm") is False:
                req2 = requests.get(self.FFPROBE_URL)
                with open('./ffprobe.wasm', 'wb') as ffprobe:
                    ffprobe.write(req2.content)
                ffprobe.close()

            if os.path.exists("./ffmpeg.wasm") is False:
                req1 = requests.get(self.FFMPEG_URL)
                with open('./ffmpeg.wasm', 'wb') as ffmpeg:
                    ffmpeg.write(req1.content)
                ffmpeg.close()
        subprocess.run("jump shortcuts")

    def erase_dependencies(self):
        subprocess.run("pip uninstall -y youtube-dl")
        subprocess.run("pip uninstall -y youtube-dl")
        subprocess.run("cd")
        subprocess.run("cd bin")
        subprocess.run("rm -f ffmpeg.wasm")
        subprocess.run("rm -f ffprobe.wasm")

        raise Exception(self.ERASED_EXC)

    def video_download(self):
        video_res = sys.argv[3]

        if video_res == "-d":
            format_opts = {
                "format": "best[ext=mp4]/best/bestvideo[ext=mp4]+bestaudio[ext*=4]/bestvideo[ext!*=4]+bestaudio[ext!*=4]",
                "playlist_items": "1-1", "outtmpl": "{}.%(ext)s".format(self.out_name)
            }
        else:
            video_fps = sys.argv[4]
            format_opts = {
                "format": "bestvideo[ext=mp4][height>={0}][fps>={1}]+bestaudio[ext*=4]/bestvideo[ext=mp4][height>={0}][fps<={1}]+bestaudio[ext*=4]/bestvideo[ext!*=4][height>={0}][fps>={1}]+bestaudio[ext!*=4]/bestvideo[ext!*=4][height>={0}][fps<={1}]+bestaudio[ext!*=4]/bestvideo[ext=mp4][height<={0}][fps>={1}]+bestaudio[ext*=4]/bestvideo[ext=mp4][height<={0}][fps<={1}]+bestaudio[ext*=4]/bestvideo[ext!*=4][height<={0}][fps>={1}]+bestaudio[ext!*=4]/bestvideo[ext!*=4][height<={0}][fps<={1}]+bestaudio[ext!*=4]/best[ext=mp4][height>={0}][fps>={1}]/best[ext=mp4][height>={0}][fps<={1}]/best[ext!*=4][height>={0}][fps>={1}]/best[ext!*=4][height>={0}][fps<={1}]/best[ext=mp4][height<={0}][fps>={1}]/best[ext=mp4][height<={0}][fps<={1}]/best[ext!*=4][height<={0}][fps>={1}]/best[ext!*=4][height<={0}][fps<={1}]".format(
                    video_res, video_fps), "playlist_items": "1-1", "outtmpl": "{}.%(ext)s".format(self.out_name)
            }
        try:
            self.single_ytdl(format_opts)
        except:
            raise Exception(self.DERROR_EXC)

    def audio_download(self):
        format_opts = {"format": "bestaudio[ext*=4]/bestaudio[ext=mp3]/best[ext=mp4]/best", "playlist_items": "1-1",
                       "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}],
                       "outtmpl": "{}.%(ext)s".format(self.out_name)}
        try:
            self.single_ytdl(format_opts)
        except:
            raise Exception(self.DERROR_EXC)

    def single_ytdl(self, format_opts):
        with youtube_dl.YoutubeDL(format_opts) as vidObj:
            meta_data = vidObj.extract_info(self.media_url, download=False)
            vid_title = meta_data.get("title", None)
            vidObj.download([self.media_url])
        re_pattern = re.compile(self.out_name + "\.[\w]{2,4}")
        file_name = re_pattern.search(subprocess.getoutput("ls").replace("\n", " ")).group(0)
        subprocess.run("open shortcuts://run-shortcut?name=SW-DLT&input=text&text=OUTPUT.{0}.TITLE.{1}".format(file_name, urllib.parse.quote(vid_title)))
        return

    def gallery_download(self):
        gallery_range = sys.argv[3]
        gallery_urls = None
        if gallery_range == "-all":
            gallery_urls = subprocess.getoutput("gallery-dl -G {}".format(self.media_url)).splitlines()
        else:
            gallery_urls = subprocess.getoutput(
                "gallery-dl -G {0} --range '{1}'".format(self.media_url, gallery_range)).splitlines()

        media_count = 0
        ext = ""
        subprocess.run("mkdir {}".format(self.out_name))
        subprocess.run("cd {}".format(self.out_name))

        for url in gallery_urls:
            if url.startswith("http"):
                media_get = requests.get(str(url))
                ext = mimetypes.guess_extension(media_get.headers['content-type'])

                media_count = media_count + 1
                with open('MEDIA_{0}{1}'.format(media_count, ext), 'wb') as media:
                    media.write(media_get.content)
                media.close()

        if media_count < 1:
            subprocess.run("jump shortcuts")
            subprocess.run("rm -r -f {}".format(self.out_name))
            raise Exception(self.DERROR_EXC)

        elif media_count < 2:
            subprocess.run("mv {0} $SHORTCUTS/{1}".format("MEDIA_" + str(media_count) + ext, self.out_name + ext))
            subprocess.run("rm -r -f {}".format(self.out_name))
            subprocess.run(
                "open shortcuts://run-shortcut?name=SW-DLT&input=text&text=OUTPUT.{0}.TITLE.{0}".format(self.out_name + ext))
        else:
            subprocess.run("jump shortcuts")
            shutil.make_archive(self.out_name, "zip", self.out_name)
            subprocess.run("rm -r -f {}".format(self.out_name))
            subprocess.run(
                "open shortcuts://run-shortcut?name=SW-DLT&input=text&text=OUTPUT.{0}.TITLE.{0}".format(self.out_name + ".zip"))

    def playlist_download(self):
        playlist_type = sys.argv[3]
        format_opts = None

        if playlist_type == "-v":
            format_opts = {"format": "best[ext=mp4]/best", "outtmpl": "{}/%(title)s.%(ext)s".format(self.out_name)}
        else:
            format_opts = {"format": "bestaudio[ext*=4]/bestaudio[ext=mp3]/best[ext=mp4]/best",
                           "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}],
                           "outtmpl": "{}/%(title)s.%(ext)s".format(self.out_name)}

        try:
            with youtube_dl.YoutubeDL(format_opts) as plObj:
                meta_data = plObj.extract_info(self.media_url, download=False)
                pl_title = meta_data.get("title", None)
                plObj.download([self.media_url])
            shutil.make_archive(self.out_name, "zip", self.out_name)
            subprocess.run("rm -r -f {}".format(self.out_name))
            subprocess.run(
                "open shortcuts://run-shortcut?name=SW-DLT&input=text&text=OUTPUT.{0}.TITLE.{1}".format(self.out_name + ".zip", urllib.parse.quote(pl_title)))

        except:
            raise Exception(self.DERROR_EXC)


def main():
    string_msgs = {
        "video_prompt": "Downloading video, custom qualities can take longer to process...",
        "audio_prompt": "Downloading audio...",
        "playlist_prompt": "Downloading playlist, process will take longer for bigger playlists...",
        "gallery_prompt": "Downloading URLs, process will take longer for bigger albums...",
        "erase_prompt": "Deleting all dependencies, please wait...",
        "dependency_check": "SW-DLT\nChecking Dependencies..."
    }

    sw_dlt_inst = SWDLT(sys.argv[1])
    download_type = sys.argv[2]
    subprocess.run("clear")

    # Pre-download cleanup and check for utility installation
    print(string_msgs["dependency_check"])

    try:
        sw_dlt_inst.check_setup()

        subprocess.run("rm -f *-*-*-*-*-*.*")
        subprocess.run("rm -r -f *-*-*-*-*-*")
        subprocess.run("clear")

        # Download functions
        if download_type == "-v":
            print(string_msgs["video_prompt"])
            sw_dlt_inst.video_download()
        elif download_type == "-a":
            print(string_msgs["audio_prompt"])
            sw_dlt_inst.audio_download()
        elif download_type == "-p":
            print(string_msgs["playlist_prompt"])
            sw_dlt_inst.playlist_download()
        elif download_type == "-g":
            print(string_msgs["gallery_prompt"])
            sw_dlt_inst.gallery_download()
        elif download_type == "-e":
            print(string_msgs["erase_prompt"])
            sw_dlt_inst.erase_dependencies()

    except Exception as rt_ex:
        # All exceptions are handled here and sent back to the Shortcut
        subprocess.run(str(rt_ex.args[0]))
        subprocess.run("clear")
        sys.exit()

    # Post download cleaning
    subprocess.run("clear")


if __name__ == "__main__":
    main()
