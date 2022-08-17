


from selenium import webdriver
from time import perf_counter
from selenium.webdriver.common.by import By

class SongScraper:

    def __init__(self, headless_mode: bool = False):
        self.loop_time_out = 5

        options = webdriver.ChromeOptions()
        if headless_mode:
            # Options to enable headless browser:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
            options.headless = True
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument("--disable-extensions")
            options.add_argument("--proxy-server='direct://'")
            options.add_argument("--proxy-bypass-list=*")
            options.add_argument("--start-maximized")
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')

        self.browser = webdriver.Chrome(executable_path="chromedriver_win32 (2)\chromedriver.exe",
                                        options=options)

        self.browser.maximize_window()

    def parse_line(self, line):
        notes = line.find_elements(By.TAG_NAME, "text")
        for n in notes:
            if n.text in {"E", "B", "G", "D", "A"}: continue
            y = float(n.get_attribute("y"))
            if y < 0: continue
            string_index = y/12
            if string_index != int(string_index): continue
            fret_number = int(n.text)
            print(string_index, fret_number)
    def get_bars(self, song_url: str):
        LINE_CLASS_NAME = "Cw81bf" # container for each line, usually has 3 bars inside
        self.browser.get(song_url)
        self.wait_for_page()

        lines = self.browser.find_elements(By.CLASS_NAME, LINE_CLASS_NAME)
        for line in lines:
            self.parse_line(line)
    def wait_for_page(self):
        page_main = self.browser.find_elements(By.CSS_SELECTOR, "html")
        started = perf_counter()

        while len(page_main) < 1 and perf_counter() - started < self.loop_time_out:
            page_main = self.browser.find_elements(By.CSS_SELECTOR, "html")

        if len(page_main) < 1:
            return False

        else:
            return True


if __name__ == '__main__':
    url = "https://www.songsterr.com/a/wsa/blind-guardian-skalds-and-shadows-tab-s27036"
