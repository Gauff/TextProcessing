import os
import requests
from urllib.parse import urlparse, unquote
import time
import validators


class FileDownloader:
    def __init__(self, download_folder_path, max_retries=3, retry_delay=2):
        self.download_folder_path = download_folder_path
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        if not os.path.exists(download_folder_path):
            os.makedirs(download_folder_path)

    @staticmethod
    def is_valid_url(url):
        """Check if the given string is a valid URL."""
        return validators.url(url)

    def download(self, url):
        if not self.is_valid_url(url):
            print(f"Invalid URL: {url}")
            return None

        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                parsed_url = urlparse(url)
                file_name = self._get_file_name(response, parsed_url)
                file_path = self._get_unique_file_path(file_name)

                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                return {
                    'file_name': file_name,
                    'file_path': file_path
                }
            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                retries += 1
                if retries < self.max_retries:
                    print(f"Retrying... ({retries}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                else:
                    print("Max retries reached. Download failed.")
                    return None

    def clean_download_folder(self):
        try:
            for file_name in os.listdir(self.download_folder_path):
                file_path = os.path.join(self.download_folder_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print(f"Download folder '{self.download_folder_path}' cleaned successfully.")
        except Exception as e:
            print(f"Error cleaning download folder: {e}")

    def _get_file_name(self, response, parsed_url):
        # Default to the last part of the URL path
        file_name = os.path.basename(unquote(parsed_url.path))

        # Override if 'Content-Disposition' header is present and has a valid filename
        if 'Content-Disposition' in response.headers:
            content_disposition = response.headers['Content-Disposition']
            if 'filename=' in content_disposition:
                file_name = content_disposition.split('filename=')[-1].strip('\"')

        if not file_name:
            file_name = "downloaded_file"

        return file_name

    def _get_unique_file_path(self, file_name):
        base, extension = os.path.splitext(file_name)
        counter = 1
        unique_file_path = os.path.join(self.download_folder_path, file_name)

        while os.path.exists(unique_file_path):
            unique_file_path = os.path.join(self.download_folder_path, f"{base}_{counter}{extension}")
            counter += 1

        return unique_file_path

# Example usage:
# downloader = FileDownloader('/path/to/download/folder')
# result = downloader.download('http://example.com/file.zip')
# print(result)
# downloader.clean_download_folder()
