# Guitar Tab To Piano Sheet Converter

## Motivation & Purpose
This is a project that converts guitar tabs with multiple instruments into a single piano sheet music document. <br>
Also generates midi piano files for guitar tabs.
As a piano player who loves listening to metal, certain songs only had guitar tabs, but no piano sheets music. <br> 
So what I'm saying is yes, the whole project happened because I wanted to play Blind Guardian on the piano 

## Results
### Example Sheet Music
Piano sheet music generated automatically via an algorithm to process guitar tabs:

<td>

<table>
  <tr>
    <td> Guitar Tabs [Before] </td>
    <td>Piano Sheets [After]</td>
   </tr> 
  <tr>
    <td width="60%"> <img src="media/images/tab_example.JPG" width="100%"></td>
    <td>
        <img src="media/images/Skalds%20and%20Shadows%20PIano%20Sheet%20Music1024_1.jpg">
        <img src="media/images/Skalds%20and%20Shadows%20PIano%20Sheet%20Music1024_1.jpg">
    </td>
   </tr> 
</table>

[Click here to see full piano sheet pdf](/media/sheet_music_results/Skalds%20and%20Shadows%20PIano%20Sheet%20Music.pdf)

### Example Visualized Midi [click on image to play video]
[![Watch the video](https://img.youtube.com/vi/XBCvDiO-7Nw/maxresdefault.jpg)](https://youtu.be/XBCvDiO-7Nw)
[Click here or the image to open video](https://youtu.be/XBCvDiO-7Nw)


## How to Run

```python
from src.midi_utils import convert_multiple_pieces_to_midi
url1 = "https://www.songsterr.com/a/wsa/lorna-shore-sun-eater-tab-s510139"
url2 = "https://www.songsterr.com/a/wsa/lorna-shore-sun-eater-tab-s510139t1" 
self = SongScraper()

#reading the notes from the songsterr url:
p1 = self.get_piece(url1, line_limit = 12, tempo_bpm = 140) # get first 12 lines at 140 bpm
p2 = self.get_piece(url2, line_limit = 12, tempo_bpm = 140) # get first 12 lines at 140 bpm

#cleaning up the web scraping:
self.browser.close()

# adjusting volume for a given piece:
p2.volume_percentage = 0.8 #the left hand being slightly quieter makes this piece better in my opinion

# merging multiple midi files and saving them into a single midi file titled "Sun Eater final"
convert_multiple_pieces_to_midi([p1, p2], "Sun Eater final")

# saving the individual midi files as well:
p2.save_as_midi("Sun Eater Tab 2")
p1.save_as_midi("Sun Eater Tab 1")

# Once you have the midi files generated, you can basically do anything you want with the song
# (sheet music, visualizing, etc. all accept midi as input so the possibilites are endless)

```