# Music-Sorter
17/04/2023

## Installation

Open up the python file and insert your desired folder directories for "check_folder" and "save_folder". The check folder is where it looks for files needing to be sorted and the save folder is where it saves the sorted files. Check "Dependencies" section to ensure all required packages are installed.

# Functionality

When run, this program looks in the "check_folder" for any mp3, flac, and jpg files. If flac files are found, they are processed into mp3 files using concurrency in batches of 10 files. The program sorts the files into 4 seperate folders in the "save_folder" directory: mp3, flac, master, and album covers. Jpgs goes into the album cover folder, mp3s into the mp3 folder, flacs into the flac folder and the best version (flac > mp3) into the master folder. The master folder is meant to be the folder you load into your desired music player as it will contain the best version of each song that you have. (Note: if a better version of the same song is entered into the database, the better version will replace the old one in the master folder). In the mp3, flac, and master folders, songs are sorted into folders named "{album} - {artist}" as pulled from the metedata of the song file. After running, type "exit" into the prompt to close the console.

# Limitations

This program relies on metedata of the individual song files to sort, so if the metedata is missing, it needs to be entered manually before the program is run. The metedata may not always be accurate, depending on where the files are sourced from, so some quirks are possible. Songs/artist/album names containing special characters will be cleansed of these characters to avoid impermissible file names. 

# Dependencies

The following packages are required to run and can be installed with pip:

- eyeD3
- mutagen

All other imports should be included in the Python standard library.

# License

Copyright © 2023 Connor Chan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
