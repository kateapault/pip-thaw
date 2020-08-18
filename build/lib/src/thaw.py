#!/usr/local/bin/python3
"""
Thaw identifies libraries in your requirements.txt file that are out of date.
Run thaw to generate a report detailing which libraries are out of date and where
those libraries are used in your project.

Requires Python 3.x

Installation::
    pip install thaw

Usage::
    $ python -m thaw
"""
import argparse
from datetime import datetime as dt
import os
import platform
import subprocess
import sys
from urllib import request


# --------------------------------------------
# SETTINGS -----------------------------------
# --------------------------------------------

logfile = "thaw_report.txt"

class WrongAssumptionError(Exception):
    def __init__(self,expression,message):
        self.expression = expression
        self.message = message

# --------------------------------------------
# HELPERS ------------------------------------
# --------------------------------------------

def version_update_scale(old_version_string, new_version_string):
    """"
    takes in version numbers old_version and new_version as strings, compares them, 
    and returns "major" "minor" or "micro" to indicate scale of update required to get to new.
    Returns None if the versions are the same
    
    major -> 1.x to 2.x
    minor -> 1.4 to 1.7
    micro ->  1.4.3 to 1.4.4
    """
    old_version = old_version_string.split('.')
    new_version = new_version_string.split('.')
    
    if old_version[0] != new_version[0]:
        return "major"
    elif old_version[1] != new_version[1]:
        return "minor"
    elif old_version == new_version:
        return None
    else:
        return "micro"

# --------------------

def library_instance_not_subword(library,line):
    '''
    returns True if library is indeed in line, False if it's part of another word, raises error if library name is not found in string
    
    ex:
    check_library_instance_isnt_subword('os','pathname = os.path.dirname("file")')
    >> True
    check_library_name_isnt_subword('os', 'total_cost = item_price + tax')
    >> False
    '''   
    library_name_start_ind = line.find(library)

    if library_name_start_ind == -1:
        raise WrongAssumptionError("library_instance_not_subword","library name not found in line")
    elif library_name_start_ind > 0:
        character_before = line[library_name_start_ind - 1]
    else: 
        character_before = None
    
    if character_before and character_before not in ' .:()[]{}=':
        return False 
    
    library_name_end_ind = library_name_start_ind + len(library) - 1
    if library_name_end_ind < len(line) - 1:
        character_after = line[library_name_end_ind + 1]
    else:
        character_after = None

    if character_after and character_after not in ' .:()[]{}=':
        return False 

    return True


# --------------------

def check_line_for_new_variable(library_name,line_string):
    '''
    Returns empty list if there is no variable assignment in the line string, 
    returns list with the variable name(s) if there is variable assignment.
    '''
    if library_name not in line_string:
        raise WrongAssumptionError('check_line_for_new_variable',"Keyword or library name not found in line")
    elif '=' not in line_string:
        return []
    else:
        return [line_string.split('=')[0].strip()]
    
# --------------------------------------------
# PYPI SEARCH --------------------------------
# --------------------------------------------

def hacky_parse_for_library_title(html_string):
    classname_start = html_string.find("package-header__name")
    
    inner_start = html_string[classname_start:].find(">")
    text_start = inner_start + classname_start + 1
    
    inner_end = html_string[classname_start:].find("<")
    text_end = inner_end + classname_start
    
    return html_string[text_start:text_end].strip()

# ----------------------

def get_latest_version(library_name):
    url = f"https://pypi.org/project/{library_name}/"
    result = request.urlopen(url)
    binary_data = result.read()
    data = binary_data.decode('utf-8')
    
    fulltitle = hacky_parse_for_library_title(data)
    try: 
        name, version = fulltitle.split(' ')
        return version
    except:
        print("something went wrong - can't split name and title")


# --------------------------------------------
# PROJECT SEARCH -----------------------------
# --------------------------------------------

def check_file_for_library(filename,library):
    '''
    inputs: str:filename, str:library name
    outputs: list containing line #s (not counting 'import x') that the library is explicity in
    '''
    f = open(filename)
    i = 0
    imported = False
    words_to_check = [library]
    affected_lines = []
    for line in f:
        line_text = str(line)
        i += 1
        if 'import' in line_text and library in line_text:
            imported = True
            if '#' in line_text:
                line_text = line_text.split('#')[0].strip()
            if 'as' in line_text:
                words_to_check = [line_text.split(' as ')[1].strip()]
            elif 'from' in line_text:
                modules = line_text.split('import')[1].strip()
                if ',' in modules:
                    for mod in modules.split(','):
                        words_to_check.append(mod.strip())
                else:
                    words_to_check.append(modules)
        elif imported:
            for keyword in words_to_check:
                if '#' in line_text:
                    if keyword in line_text.split('#')[0] and i not in affected_lines:
                        affected_lines.append(i)
                        words_to_check += check_line_for_new_variable(keyword,line_text)
                elif keyword in line_text and i not in affected_lines:
                    affected_lines.append(i)
                    words_to_check += check_line_for_new_variable(keyword,line_text)
    f.close()
    
    return affected_lines

def search_directory_for_library(library):
    dir_path = os.getcwd()
    affected_files = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                filepath = root + '/' + file
                affected_lines = check_file_for_library(filepath,library)
                if len(affected_lines) > 0:
                    affected_files.append({'file':filepath,'lines':affected_lines})

    return affected_files


# --------------------------------------------
# REPORT -------------------------------------
# --------------------------------------------
    
    
# --------------------------------------------
# MAIN ---------------------------------------
# --------------------------------------------

def main():

    scales = {
        "major": {
            "count":0,
            "libraries":[],
        },
        "minor": {
            "count":0,
            "libraries":[],
        },
        "micro": {
            "count":0,
            "libraries":[],
        }
    }
        
    affected_by_outdated_libraries = {}
    report_time = f"thaw report run {dt.now().strftime('%m-%d-%y %H:%M:%S')}\n"
    report_body = ""
    
    try:
        requirements = open("requirements.txt")
        log = open(logfile,"a+")
        
        for line in requirements:
            if "==" in line:
                library, current_version = line.strip().split("==")
                latest_version = get_latest_version(library)
                scale = version_update_scale(current_version,latest_version)
                if scale:
                    scales[scale]["count"] += 1
                    scales[scale]["libraries"].append(library)
                    affected_by_outdated_libraries[library] = search_directory_for_library(library)
                    version_change = current_version + ' >> ' + latest_version
                    report_body += f"\t*{library:<40} | {version_change:<20} | {len(affected_by_outdated_libraries[library])} files affected\n"
                else:
                    report_body += f"\t{library:<41} | {current_version}, no update needed\n"
            else:
                report_body += f'\t{line.strip():<41} | no version requirement\n'
        cutoff = len(os.getcwd()) + 1
        report_summary = ""
        major = scales['major']['count']
        minor = scales['minor']['count']
        micro = scales['micro']['count']
        print(f"{major + minor + micro} TOTAL updates")
        report_summary += f"{major + minor + micro} total updates: "
        print(f"{major} MAJOR updates")
        report_summary += f"{major} MAJOR updates, "
        print(f"{minor} MINOR updates")
        report_summary += f"{minor} MINOR updates, "
        print(f"{micro} MICRO updates")
        report_summary += f"{micro} MICRO updates\n"
        report_summary += '\nMajor updates:'
        for lib in scales['major']['libraries']:
            report_summary += f"\n[ ]{lib}"
            for affected in affected_by_outdated_libraries[lib]:
                report_summary += f"\n    {affected['file'][cutoff:]}"
                report_summary += f"\n        {affected['lines']}"
        report_summary += '\n\nMinor updates:'
        for lib in scales['minor']['libraries']:
            report_summary += f"\n[ ]{lib}"
            for affected in affected_by_outdated_libraries[lib]:
                report_summary += f"\n    {affected['file'][cutoff:]}"
                report_summary += f"\n        {affected['lines']}"
        report_summary += '\n\nMicro updates:'
        for lib in scales['micro']['libraries']:
            report_summary += f"\n[ ]{lib}"
            for affected in affected_by_outdated_libraries[lib]:
                report_summary += f"\n    {affected['file'][cutoff:]}"
                report_summary += f"\n        {affected['lines']}"
            
            
        log.write(report_time)
        log.write(report_body)
        log.write("\n")
        log.write(report_summary)
        log.write("\n\n\n\n\n")
        
        requirements.close()
        log.close()
    
    except FileNotFoundError:
        print("No requirements file found - please run thaw in the top level of your project")    