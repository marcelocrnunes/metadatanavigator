# Metadata Navigator 

Use this tool to navigate and query your AWS EC2 instance's metadata.

## Getting Started
```
./mnavigator.py -h
usage: mnavigator.py [-h] [-d] [-j] [-c] [-a] [-C [CONFIG]] [-p [PATH]]

A tool to navigate through AWS EC2 instance metadata

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug Mode
  -j, --json            JSON output mode
  -c, --color           COLOR output mode
  -a, --all             Dump all metadata
  -C [CONFIG], --config [CONFIG]
                        Config file path [default mnavigator.yaml]
  -p [PATH], --path [PATH]
                        Metadata PATH for pipe output mode [Disables
                        INTERATIVE mode][DEFAULT ROOT]

```

```
./mnavigator.py
Metadata Navigator
===================

INTERATIVE MODE:
Press ENTER, l, or list to view available metadata options.
Enter metadata name to view it's current value.
Enter path name with trailling slash to navigate further on the categories
Enter "b" or "back" to go back to previous metadata category
Enter "r" or "reset" to go to root path
Enter "c" or "clear" to clear the screen
Enter "q" or "quit" to quit.
Press "Ctrl-t" to toggle json mode (-j option on the commandline)
Press "Ctrl-y" to toggle color mode (-c option on the commandline)

PIPE MODE:
Call the command with the "-p" argument. 

DUMP all metadata: 
Call the command with the "-a" argument.

Call the command with "-h" for usage help.
```

For a more in depth view of the tool: 

[![asciicast](https://asciinema.org/a/tw1nOpXEZzJoqZNHDzwp3VDMs.png)](https://asciinema.org/a/tw1nOpXEZzJoqZNHDzwp3VDMs)

### Prerequisites

* Python>=3 (Should work on Python>=2.7. No promises...)
* Pygments==2.1.1
* termcolor==1.1.0
* prompt_toolkit==1.0.15
* requests==2.18.4
* PyYAML==3.12

### Installing

```
git clone https://github.com/marcelocrnunes/metadatanavigator.git
cd metadatanavigator/
pip install -r requirements.txt 
chmod +x mnavigator
```

## Authors

* **Marcelo Nunes** - ** - [marcelocrnunes](https://github.com/marcelocrnunes)

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Amit Upadhyay [Python For Programmers](https://amitu.com/python/toc/) 
* Amjith Ramanujam [Awesome Command Line Tools PyCon 2017](https://www.youtube.com/watch?v=hJhZhLg3obk)
