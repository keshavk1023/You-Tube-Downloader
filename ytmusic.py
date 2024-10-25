import pytube
import sys

class YouTubeAudioDownloader:
    def __init__(self):
        self.url = str(input("Enter the URL of the video: "))
        self.youtube = pytube.YouTube(self.url, on_progress_callback=YouTubeAudioDownloader.on_progress)
        self.show_title()

    def show_title(self):
        print(f"Title: {self.youtube.title}\n")
        self.show_streams()

    def show_streams(self):
        self.stream_no = 1
        self.audio_streams = self.youtube.streams.filter(only_audio=True)
        for stream in self.audio_streams:
            print(f"{self.stream_no} => abr: {stream.abr} / type: {stream.type}")
            self.stream_no += 1
        self.choose_stream()

    def choose_stream(self):
        self.choose = int(input("Please select one: "))
        self.validate_choose_value()

    def validate_choose_value(self):
        if self.choose in range(1, self.stream_no):
            self.get_stream()
        else:
            print("Please enter a correct option from the list.")
            self.choose_stream()

    def get_stream(self):
        self.stream = self.audio_streams[self.choose - 1]
        self.get_file_size()

    def get_file_size(self):
        global file_size
        file_size = self.stream.filesize / 1000000  # Convert to MB
        self.get_permission_to_continue()

    def get_permission_to_continue(self):
        print(f"\nTitle: {self.youtube.title} \nAuthor: {self.youtube.author} \nSize: {file_size:.2f} MB \nType: {self.stream.type}\n")
        if input("Do you want to download it? (default = (y)es) or (n)o ") == "n":
            self.show_streams()
        else:
            self.main()

    def download(self):
        self.stream.download()
        print("Download completed!")

    @staticmethod
    def on_progress(stream=None, chunk=None, remaining=None):
        file_downloaded = file_size - (remaining / 1000000)
        print(f"Downloading ... {file_downloaded / file_size * 100:.2f}% [{file_downloaded:.1f}MB of {file_size:.1f}MB]", end="\r")

    def main(self):
        try:
            self.download()
        except KeyboardInterrupt:
            print("Canceled.")
            sys.exit(0)

if __name__ == "__main__":
    try:
        YouTubeAudioDownloader()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
