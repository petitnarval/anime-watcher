# ANIME WATCHER

## What is this ?

Anime Watcher is a python program that allows you to watch anime in your terminal like a true nerddd

## How to use it

### Install python
You need to install [Python 3.12.4](https://www.python.org/downloads/release/python-3124/). Make sure you add it to the path and install PIP (which are options to check during the installation process).

### Install MPV
It is recommended to install MPV using scoop. First install scoop by running in your PowerShell the following command:
```ps1
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

Then install MPV and youtube-dl by running this command in your CLI:
```bat
scoop bucket add extras
scoop install extras/mpv
scoop bucket add main
scoop install main/yt-dlp
```

### Install Anime Watcher
Clone this repo / download it as a zip file and unzip it somewhere on your drive.
Run the `dependrancy.bat` file to install the python dependencies.

Open a CLI, place yourself in the directory where Anime Watcher is installed, and run Anime Watcher using the followin command: `py main.py`.
For some people, this command doesn't work, and they need to use `python main.py`. Test both of them to see which one works on your system.

### Adding Anime Watcher as a command in your CLI (optional)
If you want to start Anime Watcher from aniwhere in your system (without having to change directory), follow these steps.

First, go in a folder that is listed in your path. You can use WinKey > env > Path to see the list of path folders or add one.
Then, create a file named `anime-watcher.bat` and write the following line into it:
```bat
@START py [path]main.py
```

Replace [path] with the path in which is located Anime Watcher on your drive. For example: `@START py D:\Documents\Dev\anime-watcher\main.py`

As in the last step, you may have to use `python` instead of `py` for it to work.

Then, open a CLI and type `anime-watcher`, that's it !
