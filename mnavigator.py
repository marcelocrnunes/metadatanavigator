#!/usr/bin/python3
"""
This script will handle the initial configuration using command line arguments and the YAML config file and calling the metadatanavigator functions to enable/disable debug, color and json support.
Once all configuration are set, the script will call the mnavigator function, imported from metadatanavigator, with the parameters configured by the user.
"""
from metadatanavigator import *
import yaml
import argparse


def create_parser():
    """
    Create a configuration parser and parses the commandline configuration. 
    """
    parser = argparse.ArgumentParser(description='A tool to navigate through AWS EC2 instance metadata')
    parser.add_argument("-d", "--debug", help="Debug Mode", action="store_true")
    parser.add_argument("-j", "--json", help="JSON output mode", action="store_true")
    parser.add_argument("-c", "--color", help="COLOR output mode", action="store_true")
    parser.add_argument("-a", "--all", help="Dump all metadata", action="store_true")
    parser.add_argument("-C", "--config", help="Config file path [default mnavigator.yaml]",nargs='?',const="mnavigator.yaml", default="mnavigator.yaml")
    parser.add_argument("-p", "--path", help="Metadata PATH for pipe output mode [Disables INTERATIVE mode][DEFAULT ROOT]",nargs='?', const="/")
    args=parser.parse_args()
    return args

def main():
    """
    Main function. Handle configuration settings and metadata navigator's main functions. 
    """
    try:
        args=create_parser()

        with open(args.config,'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        if args.debug or cfg['debug']==True:
            """
            Enable debug.
            """
            setdebugstatus(True)
            print ("ARGUMENTS: ",args)
            print ("LOADED CONFIG: ", cfg)

        if args.json or cfg['jsonenable']:
            """
            Enable JSON output.
            """
            setjsonstatus()

        if args.color or cfg['colorenable']:
            """
            Enable COLOR output.
            """
            setcolorstatus()

        if args.path:
            """Enable PIPE mode"""
            pipemode=True
            pipemodepath=args.path
        else:
            """Disable PIPE mode"""
            pipemode=False
            pipemodepath=None

        if args.all:
            """Dump all metadata"""
            print(metadatadump())
            exit(0)

        """
        Setup the rest of the configuration, like colors for the prompt and texts.
        """
        setconfig(cfg)

        """
        Call tool's main function.
        """
        mnavigator(pipemode, pipemodepath)

    except IOError:
        print("ERROR: Could not find YAML configuration file",args.config)

    except Exception as e:
        print("ERROR: Unrecoverable error: ",e)

if __name__ == '__main__':
    main()
