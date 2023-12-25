import os, sys, subprocess, argparse, psutil
import re


def createParser():
    """
    Create instanse of a class to parse arguments from comand line
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blend', nargs = '+', required = True, help = 'type a name(names) and extension of a .blend file(files) you want to render in any order')
    parser.add_argument('-s', '--script', nargs = '+', default = '',  help = '(Optional) type a name(names) and extension of .py script(scripts) you want to launch, in order they should be executed')
    parser.add_argument('-L', action='store_true', help = '(Optional) if you want to render certain scenes. Then you will be asked to select cirtain scenes from a given list')
    return parser

def is_blender_running():
    """
    Check if blender is already oppened on the server
    """
    
    return 'blender.exe'  in (p.name() for p in psutil.process_iter())