# Bible
Read the Bible in the terminal with Python and Curses.

![Preview](preview.png)

## Installation
```shell
$ python3 -m pip install https://github.com/rwev/bible/archive/master.zip
```

## Usage 
```shell
$ bible
```
Use the arrow keys to navigate and make selections. 

## Development

Using [resurgence](http://github.com/rwev/resurgence): 

```shell
$ git clone https://github.com/rwev/bible.git
$ python3 -m pip install http://github.com/rwev/resurgence/archive/master.zip
$ cd ./bible/bible
$ resurgence -w -x "python3 main.py" -t .py
```

## TODO
- compress translation files
- select desired translations during installation
- add bookmarking
- add vim keybindings
- fuzzy-finder in selection windows
