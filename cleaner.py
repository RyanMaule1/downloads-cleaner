import os
from time import sleep
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
#directory to be monitered
source_dir = "/home/ryan/Downloads"

#Destination directories for downloads
dest_docs = "/home/ryan/Desktop/documents"
dest_music = "/home/ryan/Desktop/music"
dest_pictures = "/home/ryan/Desktop/pictures"
dest_videos = "/home/ryan/Desktop/videos"

def moveFile(dest, name, entry):
    if os.path.exists(dest + "/" + name):
        newName = name + "(copy)"
        os.rename(entry, newName)
    shutil.move(entry, dest)

class FileHandler(LoggingEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.lower().endswith(("pdf", "doc", "docx")):
                    dest = dest_docs
                    moveFile(dest, name, entry)
                elif name.endswith(("mp3","wav")):
                    dest = dest_music
                    moveFile(dest, name, entry)
                elif name.lower().endswith((".jpg", ".jpeg", ".svg", ".png")):
                    dest = dest_pictures
                    moveFile(dest, name, entry)
                elif name.lower().endswith((".mp4", ".mov")):
                    dest = dest_videos
                    moveFile(dest, name, entry)


#code used by watchdog library to moniter our downloads dir for changes
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()