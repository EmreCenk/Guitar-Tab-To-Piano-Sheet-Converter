


from selenium import webdriver
from time import perf_counter
from selenium.webdriver.common.by import By
from src.MusicAbstractions import GuitarTabNote, PianoNote, Piece, Bar
from typing import *
from src.PathCommands import PathCommandParser, BeatCorrecter

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

        # self.browser.maximize_window()
    def get_line_notes(self, line) -> Bar:
        print("get_line_notes()")
        notes = line.find_elements(By.TAG_NAME, "text")
        print("got 'notes', this many:", len(notes), "on this line")

        piano_notes = {}
        for n in notes:
            if n.text in {"E", "B", "G", "D", "A"}: continue
            y = float(n.get_attribute("y"))
            x = float(n.get_attribute("x"))
            if y < 0: continue
            string_index = y/12
            if string_index != int(string_index): continue
            string_index = int(string_index)
            fret_number = int(n.text)
            #todo: parse timings here as well (the parsing is already written, just not plugged in to this section of code)
            # print(string_index, fret_number)

            curnote = GuitarTabNote(0, fret_number, string_index).convert_to_piano_note()
            if x not in piano_notes: piano_notes[x] = [curnote]
            else: piano_notes[x].append(curnote)

        cur_bar = Bar([])
        for entry in sorted(piano_notes):
            print("is it sorted", entry, piano_notes[entry])
            cur_bar.notes.append(piano_notes[entry])
        # print("Here are notes: ")
        # for n in piano_notes: print(n.note, n.beat_length, end = "\t --- \t")
        print()
        return cur_bar

    def get_line_timings(self, line):
        timings = line.find_elements(By.TAG_NAME, "path")[1:]
        correction_command = " "
        for k in timings:
            if k.get_attribute("class") == "Bhq244":
                correction_command = k.get_attribute("d")
                break

        translation_element = line.find_elements(By.CLASS_NAME, "Bhq8x")
        if len(translation_element) > 0:
            translation_string = translation_element[0].get_attribute("transform")
            translation_string = translation_string[translation_string.find("(") + 1: translation_string.find(")")].split(",")
            translation = (float(translation_string[0]), float(translation_string[1]))
        else:
            translation = (0, 0)



        print("correction", correction_command)
        times = []
        for k in timings:
            # print(k.get_attribute("class"))
            if k.get_attribute("class") == "Gy73":
                path_command = k.get_attribute("d")
                parser = PathCommandParser()
                # print(path_command)
                beat_lengths = parser.path_command_to_beats(path_command, correction_command=correction_command, translation = translation)
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
            print("equating number", i, len(beat_times), len(piano_bar.notes))
            for j in range(len(piano_bar.notes[i])):
                piano_bar.notes[i][j].beat_length = beat_times[i]
        print("done equating")
        return piano_bar

    def get_piece(self, song_url: str, line_limit: int = 10000, tempo_bpm: int = 60) -> Piece:
        LINE_CLASS_NAME = "Cw81bf" # container for each line, usually has 3 bars inside
        self.browser.get(song_url)
        self.wait_for_page()
        self.browser.implicitly_wait(2)
        print("opened url:", song_url)

        lines = self.browser.find_elements(By.CLASS_NAME, LINE_CLASS_NAME)
        print(f"got this lines, this many in fact: {len(lines)}")

        bars = []
        W = len(lines)
        print("new W (first):", W)
        i = 0
        while i < W and i < line_limit:

        # for i in range(len(lines)):
            print("on line", i)
            current_bar = self.parse_line(lines[i])
            bars.append(current_bar)
            i += 1
            lines = self.browser.find_elements(By.CLASS_NAME, LINE_CLASS_NAME)
            W = len(lines)
            print("new W:", W)
            print("\n\n")
        return Piece(bars, tempo_bpm = tempo_bpm)

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
    from src.midi_utils import convert_multiple_pieces_to_midi
    url1 = "https://www.songsterr.com/a/wsa/blind-guardian-skalds-and-shadows-tab-s27036"
    url2 = "https://www.songsterr.com/a/wsa/blind-guardian-skalds-and-shadows-tab-s27036t1"
    url3 = "https://www.songsterr.com/a/wsa/blind-guardian-skalds-and-shadows-tab-s27036t2"
    self = SongScraper()
    linelim = 5
    p1 = self.get_piece(url1, line_limit = linelim, tempo_bpm = 90) #get first 12 lines
    # p2 = self.get_piece(url2, line_limit = linelim, tempo_bpm = 90) #get first 12 lines
    p3 = self.get_piece(url3, line_limit = linelim, tempo_bpm = 90) #get first 12 lines
    # p3.tempo_bpm = 45
    # p1.convert_to_midi_file().save("p1")
    print("done")
    convert_multiple_pieces_to_midi([p1, p3], "nothing_broken_hopefully")
    p3.convert_to_midi_file().save("p3")
    # p1.convert_to_midi_file().save("ye")
    # midi_file1 = p1.convert_to_midi_file()
    # midi_file1.save("yes0")
    # midi_file2 = p2.convert_to_midi_file(midi_file1)
    # midi_file2.save("yes2")
