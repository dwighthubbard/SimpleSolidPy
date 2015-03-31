__author__ = 'Dwight Hubbard'
"""
Parse openscad script as a string
"""
import logging
import re


logger = logging.getLogger(__name__)
logger.debug('Module loading')


# Single line manipulations
def convert_module_to_def(openscad_line, current_indent, indent, infunc):
    """
    Convert an openscad module statement into a python def
    """
    if openscad_line.startswith('module '):
        openscad_line = openscad_line.replace('module ', 'def ', 1).replace(')', '):', 1)
    return openscad_line, current_indent, infunc

def convert_items_to_arguments(openscad_line, current_indent, indent, infunc):
    """
    Convert items that should be arguments into arguments
    """
    temp = openscad_line.split('(')
    if temp and temp[0].strip() in ['rotate', 'translate', 'union', 'scale']:
        # Remove the trailing ) so the following become arguments
        openscad_line = temp[0] + '(\n' + ' ' * (current_indent + 4)  + '('.join(temp[1:])
        openscad_line = openscad_line.replace(')', ', ')
        infunc = True
        #current_indent += 4
    return openscad_line, current_indent, infunc

def convert_braces_to_indent(openscad_line, current_indent=0, indent=4, infunc=False):
    """
    Convert curly braces in openscad to python indentation
    """
    new_line_words = []
    for word in openscad_line.split():
        if word == '{':
            current_indent += indent
            word = '\n' + ' ' * current_indent
        elif word == '}':
            current_indent -= indent
            if current_indent < 0:
                current_indent = 0
            if infunc:
                word = '\n' + ' ' * current_indent + ')'
            else:
                word = '\n' + ' ' * current_indent
        new_line_words.append(word)

    return ' '.join(new_line_words), current_indent, infunc


def convert_remove_trailing_semicolons(openscad_line, current_indent=0, indent=4, infunc=False):
    return openscad_line.rstrip().rstrip(';'), current_indent, infunc


# Whole script manipulations
def normalize(openscad_script):
    """
    Convert the openscad script to a common format

    Converts \r to newline

    Removes whitespace at the start and ends of lines

    returns a list
    """
    # Convert \r to \n and remove extra blank lines
    openscad_script = openscad_script.replace('\r', '\n')
    openscad_script = openscad_script.replace('\n\n', '\n')

    # Strip whitespace
    return [line.strip() for line in openscad_script.split('\n')]


def cleanup_remove_blank_lines(openscad_string):
    """
    Remove extra blank lines from the python script
    """
    cleaned_string = ''
    for line in openscad_string.split('\n'):
        if line.strip():
            cleaned_string += line + '\n'
    return cleaned_string.replace('\ndef', '\n\ndef')


def make_one_function_per_line(openscad_script):
    result = ''
    for line in openscad_script.split('\n'):
        temp = line.split(')')
        if len(temp) > 1:
            # Got multiple functions on a line
            new_line = ''
            looking_for_next = False
            for c in line:
                if c == ')':
                    if looking_for_next:
                        new_line += ')\n}'
                    else:
                        new_line += ')\n{'
                    looking_for_next = True
                else:
                    new_line += c
            line = new_line

        line = line.replace(')', ')\n')
        result += line.rstrip('\n') + '\n'
    return result


def remove_scad_comments_to_python(openscad_script):
    """
    Remove openscad comments since they aren't in a format python likes
    """
    # TODO: Make this convert the comments instead of removing them
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, openscad_script)


def convert(openscad_script, indent=4):
    """
    Convert a string containing an openscad script into a string of python code
    """
    # TODO: Handle converting and passing special variables
    current_indent = 0
    infunc = False
    python_script = ''

    openscad_script = 'from openscad_blender.functions import *\n\n' + remove_scad_comments_to_python(make_one_function_per_line(openscad_script))
    for line in normalize(openscad_script):
        line, current_indent, infunc = convert_remove_trailing_semicolons(line, current_indent, indent, infunc)
        line, current_indent, infunc = convert_module_to_def(line, current_indent, indent, infunc)
        python_script += ' ' * current_indent
        line, current_indent, infunc = convert_braces_to_indent(line, current_indent, indent, infunc)
        line, current_indent, infunc = convert_items_to_arguments(line, current_indent, indent, infunc)
        python_script += line + '\n'

    return cleanup_remove_blank_lines(python_script)


def execute(openscad_script):
    """
    Convert an openscad script from a string to python and execute it
    """
    exec(convert(openscad_script))


def include(filename):
    script = open(filename).read()
    execute(script)

