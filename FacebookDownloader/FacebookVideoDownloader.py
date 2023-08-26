from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeServices
import re
from bs4 import BeautifulSoup
import requests
import platform
import pkg_resources
import warnings
import html
import os
warnings.filterwarnings("ignore")

class FacebookVideoDownloader:

    def __init__(self, url) -> None:
        self.url = url
        self.init_driver()

    def driver_options(self):
        options = webdriver.ChromeOptions()
        env = self.detect_os()
        if env == 'DYNO':
            options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
        else:
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--no-first-run")
            options.add_argument("headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-default-browser-check")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-xss-auditor")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--log-level=1")
            options.add_experimental_option("prefs", 
                {
                    "profile.default_content_setting_values.notifications": 2 
                }
            )
        return options

    def driver_services(self):
        service = ChromeServices(self.detect_os())
        return service
    
    def detect_os(self):
        os_name = platform.system()
        if os_name == "Windows":
            return pkg_resources.resource_filename(__name__, 'webdrivers/win/chromedriver.exe')
        elif os_name == "Linux":
            return pkg_resources.resource_filename(__name__, 'webdrivers/linux/chromedriver')
        elif os_name == "Darwin":
            return pkg_resources.resource_filename(__name__, 'webdrivers/mac/chromedriver')
        elif 'DYNO' in os.environ:
            return 'DYNO'
        else:
            print("Operating system detection not supported.")
    

    def init_driver(self):
        env = self.detect_os()
        if env == 'DYNO':
            service = ChromeServices(executable_path=str(os.environ.get("CHROMEDRIVER_PATH")))
        else:
            service = self.driver_services()

        self.driver = webdriver.Chrome(service=service, options=self.driver_options())
        self.driver.get(self.url)
        self.page_soup = self.driver.page_source
        self.driver.quit()

    def get_streams(self):
        hd_url_pattern = r'browser_native_hd_url":"([^"]+)"'
        sd_url_pattern = r'browser_native_sd_url":"([^"]+)"'
        matches = re.findall(hd_url_pattern, self.page_soup)
        self.hd_url = [match.replace("\\", "") for match in matches]

        matches = re.findall(sd_url_pattern, self.page_soup)
        self.sd_url = [match.replace("\\", "") for match in matches]

        return {
            'sd_url': self.sd_url,
            'hd_url': self.hd_url
        }

    def get_title(self):
        soup = BeautifulSoup(self.page_soup, "html.parser")
        title_tag = soup.title
        if title_tag:
            title = title_tag.string
            self.title = title.split(" | Facebook")[0]
        else:
            self.title = 'Not Found'

        return title
        
    def download(self):
        response = requests.get(self.get_streams()[self.get_recommended_quality()], stream=True)
        output_file = f"Facebook Video.mp4"
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("Video downloaded successfully.")
        else:
            print("Failed to download video.")

    def get_recommended_quality(self):
        response = requests.get(self.get_streams()['hd_url'], stream=True)
        if response.status_code == 200:
            return 'hd_url'
        
        response = requests.get(self.get_streams()['sd_url'], stream=True)
        if response.status_code == 200:
            return 'sd_url'

    def get_captions(self):
        captions_url_pattern = r'captions_url":"([^"]+)"'
        matches = re.findall(captions_url_pattern, self.page_soup)
        caption_url = [match.replace("\\", "") for match in matches]
        return html.unescape(caption_url[0])
        