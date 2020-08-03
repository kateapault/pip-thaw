
"""
pip-thaw identifies packages in your requirements.txt file that are out of date.
Run pip-thaw to generate a report detailing which libraries are out of date and where
those libraries are used in your project.

Requires ``pip`` Version 9 or higher.

Installation::
    pip install pip-thaw

Usage::
    pip-thaw 
"""
from datetime import datetime as dt
import os
import subprocess
import sys
from urllib import request


# --------------------------------------------
# SETTINGS -----------------------------------
# --------------------------------------------

logfile = "thaw_report.txt"

# --------------------------------------------
# HELPERS ------------------------------------
# --------------------------------------------

def dictify_pip_list(pip_stdout):
    pip_string = pip_stdout.decode('utf-8')
    pip_arr = pip_string.split()

    pip_list_dict = {}
    i = 8
    while i < len(pip_arr):
        
        if i % 4 == 0:
            library_name = pip_arr[i]
        elif i % 4 == 1:
            library_info = {"current":pip_arr[i]}
        elif i % 4 == 2:
            library_info["latest"] = pip_arr[i]
        else:
            update_scale = version_change_scale(library_info["current"], library_info["latest"])
            print(f"{library_name}: version {library_info['current']} to version {library_info['latest']} => {update_scale} update")
            library_info["scale"] = update_scale
            pip_list_dict[library_name] = library_info
        i += 1
        
    return pip_list_dict


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

def package_instance_not_subword(package,line):
    '''
    this assumes substring package has already been found inside string line
    returns True if package is indeed in line, False if not
    ex:
    check_package_instance_isnt_subword('os','pathname = os.path.dirname("file")')
    >> True
    check_package_name_isnt_subword('os', 'total_cost = item_price + tax')
    >> False
    '''
    actual_package_instance = True
    
    package_name_start_ind = line.find(package)
    if package_name_start_ind > 0:
        character_before = line[package_name_start_ind - 1]
    else: 
        character_before = None
    if character_before and character_before not in ' .:()[]{}=':
        actual_package_instance = False

    return actual_package_instance

# --------------------------------------------
# PYPI SEARCH --------------------------------
# --------------------------------------------

def hacky_parse_for_package_title(html_string):
    classname_start = html_string.find("package-header__name")
    
    inner_start = html_string[classname_start:].find(">")
    text_start = inner_start + classname_start + 1
    
    inner_end = html_string[classname_start:].find("<")
    text_end = inner_end + classname_start
    
    return html_string[text_start:text_end].strip()


def get_latest_version(package_name):
    url = f"https://pypi.org/project/{package_name}/"
    result = request.urlopen(url)
    binary_data = result.read()
    data = binary_data.decode('utf-8')
    
    fulltitle = hacky_parse_for_package_title(data)
    name, version = fulltitle.split(' ')
    return version


# --------------------------------------------
# PROJECT SEARCH -----------------------------
# --------------------------------------------

def check_file_for_library(filename,library):
    '''
    inputs: str:filename, str:library name
    outputs: list containing line #s (not counting 'import x') that the library is explicity in
    '''
    # need to account for multiple submodules
    # need to disregard if part of something eg 'cost' variable gets caught while looking for 'os' package
    # Actually Useful and harder to code Mode: grab variables/etc made w package and identify lines using those
    f = open(filename)
    i = 0
    imported = False
    affected_lines = []
    for line in f:
        line_text = str(line)
        i += 1
        if 'import' in line_text and library in line_text:
            imported = True
            if 'as' in line_text:
                library = line_text.split('as')[1].strip()
            elif 'from' in line_text:
                library = line_text.split('import')[1].strip()
        elif imported and '#' in line_text:
            if library in line_text.split('#')[0]:
                affected_lines.append(i)
        elif imported and library in line_text:
            affected_lines.append(i)
    return affected_lines

def search_directory_for_library(library='pyshorteners'):
    dir_path = os.path.dirname(os.path.realpath(__file__))

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
    report_time = f"pip-thaw {dt.now().strftime('%m-%d-%y %H:%M:%S')}\n"
    report_body = ""
    
    try:
        log = open(logfile,"a+")
        requirements = open("requirements.txt")
        
        for line in requirements:
            if "==" in line:
                library, current_version = line.strip().split("==")
                latest_version = get_latest_version(library)
                scale = version_update_scale(current_version,latest_version)
                if scale:
                    scales[scale]["count"] += 1
                    scales[scale]["libraries"].append(library)
                    affected_by_outdated_libraries[library] = search_directory_for_library(library)
                    report_body += f"\t*{library:<40} | {current_version} >> {latest_version} | {affected_by_outdated_libraries[library]}\n"
                else:
                    report_body += f"\t{library:<41} | {current_version}, no update needed\n"
            else:
                report_body += f'\t{line.strip():<41} | no version requirement\n'

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
        
        log.write(report_time)
        log.write(report_summary)
        log.write(report_body)
        log.write("\n")
        
        requirements.close()
        log.close()
    
    except FileNotFoundError:
        print("No requirements file found - please run thaw in the top level of your project")    
if __name__ == "__main__":
    main()