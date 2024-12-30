import download
import initialize

class start:
    def download():
        chk, url, output_path, folder_path = initialize.get()
        if chk and initialize.create_folder(folder_path):
            download.start_download(url, output_path)

if __name__ == "__main__":
        start.download()