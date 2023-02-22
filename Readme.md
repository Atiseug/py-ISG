# Description

---
Python partial implementation of [Infinite-Storage-Glitch](https://github.com/DvorakDwarf/Infinite-Storage-Glitch) project and back compatible with its video-files (at least for now).   

I don't know Rust, and I'm too lazy to compile original project or to boot to linux, so I don't know all the functionality of the original project, but I'm sure Rust should be much faster than this ("blazingly fast" right? :)). This project was done and as kind of challenge for me and just for fun.

### About YouTube TOS:

---
Probably it is not forbidden to upload such videos, but who knows.  
As it was mentioned in [original project Readme](https://github.com/DvorakDwarf/Infinite-Storage-Glitch/blob/master/README.md#now-you-might-be-asking-yourself):

> YouTube might understandably get mad.  

So use this at your own risk.  

### Download video from YouTube

---
So as I understood original [Infinite-Storage-Glitch](https://github.com/DvorakDwarf/Infinite-Storage-Glitch) can download videos from YT by itself.  
This project cannot do it (well at least for now) so to download file from YouTube you can just replace `youtube` to `ssyoutube` in your URL.

# Installation

---
Tested on [Python 3.10.6](https://www.python.org/downloads/release/python-3106/)  
Run all commands inside the folder with `main.py`.


1. `python -m venv venv` to create virtual environment
2. Activate venv: 
   - Windows: `.\venv\Scripts\activate` (`(venv)` should be shown at start of line if this command worked fine)
   - bash: `source /venv/bin/activate`
3. `pip install -r requirements.txt`
4. You're ready to go.

## How to Use

---

1. Make zip archive from some of your files. Or download video which you want to convert to file.
2. Run the `main.py` (there are only 2 options each of which I think should be clear)
3. Write a path to a file/video. If the file/video is in the same folder as the `main.py` you can just type its name it should work.
4. Wait...  

You also can read [original instruction](https://github.com/DvorakDwarf/Infinite-Storage-Glitch/blob/master/README.md#how-to-use).