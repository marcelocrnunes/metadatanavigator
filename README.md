# Metadata Navigator 

Use this tool to navigate and query your AWS EC2 instance's metadata.

## Getting Started
```
./mnavigator -h
usage: mnavigator [-h] [-d] [-j] [-c] [-p [PATH]]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug Mode
  -j, --json            JSON output mode
  -c, --color           COLOR output mode
  -p [PATH], --path [PATH]
                        Metadata PATH for pipe output mode [Disables
                        INTERATIVE mode][DEFAULT ROOT]
```

```
./mnavigator
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
Call the command with the "-p" argument. Call the command with "-h" for usage help.
```

For a more in depth view of the tool: 

[![asciicast](https://asciinema.org/a/tw1nOpXEZzJoqZNHDzwp3VDMs.png)](https://asciinema.org/a/tw1nOpXEZzJoqZNHDzwp3VDMs)

### Prerequisites

Pygments==2.1.1
requests==1.2.3
prompt_toolkit==1.0.15
termcolor==1.1.0

### Installing

```
git clone https://github.com/marcelocrnunes/metadatanavigator.git
cd mnavigator/
pip -r requirements.txt 
chmod +x mnavigator
```

## Authors

* **Marcelo Nunes** - ** - [marcelocrnunes](https://github.com/marcelocrnunes)

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Amit Upadhyay [Python For Programmers](https://amitu.com/python/toc/) 
* Amjith Ramanujam [Awesome Command Line Tools PyCon 2017](https://www.youtube.com/watch?v=hJhZhLg3obk)
