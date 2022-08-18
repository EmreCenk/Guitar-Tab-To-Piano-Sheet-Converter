


from selenium import webdriver
from time import perf_counter
from selenium.webdriver.common.by import By
from src.MusicAbstractions import GuitarTabNote, PianoNote, Piece, Bar
from typing import *
from src.PathCommands import PathCommandParser

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
        try:
            self.browser = webdriver.Chrome(executable_path="chromedriver_win32 (2)\chromedriver.exe",
                                            options=options)
        except:
            self.browser = webdriver.Chrome(executable_path="src\chromedriver_win32 (2)\chromedriver.exe",
                                            options=options)

        self.browser.maximize_window()
    def get_line_notes(self, line) -> Bar:
        print("get_line_notes()")
        notes = line.find_elements(By.TAG_NAME, "text")
        print("got 'notes', this many:", len(notes), "on this line")

        piano_notes = []
        for n in notes:
            if n.text in {"E", "B", "G", "D", "A"}: continue
            y = float(n.get_attribute("y"))
            if y < 0: continue
            string_index = y/12
            if string_index != int(string_index): continue
            string_index = int(string_index)
            fret_number = int(n.text)
            #todo: parse timings here as well (the parsing is already written, just not plugged in to this section of code)
            # print(string_index, fret_number)
            piano_notes.append(GuitarTabNote(0, fret_number, string_index).convert_to_piano_note())
        print("Here are notes: ")
        for n in piano_notes: print(n.note, n.beat_length, end = "\t --- \t")
        print()
        return Bar(piano_notes)

    def get_line_timings(self, line):
        timings = line.find_elements(By.TAG_NAME, "path")[1:]
        times = []
        for k in timings:
            print(k.get_attribute("class"))
            if k.get_attribute("class") != "Gy73": continue
            path_command = k.get_attribute("d")
            parser = PathCommandParser()
            beat_lengths = parser.path_command_to_beats(path_command)
            for b in beat_lengths: times.append(b)

        return times

    def parse_line(self, line) -> Bar:
        print("parsing line...")
        piano_bar = self.get_line_notes(line)

        print("starting beat times")
        beat_times = self.get_line_timings(line)
        print("done beat times, equating:")
        print(len(piano_bar.notes), len(beat_times), "<- (these should be equal)")
        for i in range(len(piano_bar.notes)):
            print("equating number", i)
            piano_bar.notes[i].beat_length = beat_times[i]
        print("done equating")
        return piano_bar

    def get_piece(self, song_url: str) -> Piece:
        LINE_CLASS_NAME = "Cw81bf" # container for each line, usually has 3 bars inside
        self.browser.get(song_url)
        self.wait_for_page()
        self.browser.implicitly_wait(2)
        print("opened url:", song_url)

        lines = self.browser.find_elements(By.CLASS_NAME, LINE_CLASS_NAME)
        print(f"got this lines, this many in fact: {len(lines)}")

        bars = []
        for i in range(len(lines)):
            print("on line", i)
            current_bar = self.parse_line(lines[i])
            bars.append(current_bar)
            print("\n\n")
        return Piece(bars)

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
    self = SongScraper()
    p = self.get_piece(url)
