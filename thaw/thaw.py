#!/usr/local/bin/python3
"""
Thaw searches through your project and generates a report detailing which libraries
are out of date and where those libraries are used in your project.

Requires Python 3.3 or later

Installation::
    $ pip install thaw

Usage::
    $ python -m thaw ~/directory/to/search [-h] [-i IMPORTS] [-l LIBRARY] [-o OUT] [-v VERBOSE]
    
Flags::
    --imports                   => searches for libraries in import statements rather than requirements.txt file
    --library [lib1 lib2 ...]   => searches for specified library/ies regardless of version status
    --out [directory path]      => creates report .txt file in specified directory
    --verbose                   => includes line text in report, not just line numbers where outdated libraries are used
"""
import argparse
from datetime import datetime as dt
import os
import platform
import subprocess
import sys
from urllib import request

class WrongAssumptionError(Exception):
    def __init__(self,expression,message):
        self.expression = expression
        self.message = message

# -----------------------------------------------------------
# HELPER FUNCTIONS ------------------------------------------
# -----------------------------------------------------------

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

# -----------------------------------------------------------

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


# -----------------------------------------------------------

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
    
# -----------------------------------------------------------
# PYPI / LOCAL SEARCH ---------------------------------------
# -----------------------------------------------------------

def get_library_source(library,project_dir):
    '''
    Takes in library name string and project directory location
    Outputs "pypi", "local", or "other" depending on whether the library 
    is a dependency found on pypi, a local dependency within the project, 
    or something else/not found in the project
    '''
    local = False
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file == f"{library}.py":
                local = True
    if local:
        return "local"
    else:
        url = f"https://pypi.org/project/{library}/"
        try:
            result = request.urlopen(url)
            return "pypi"
        except:
            return "other"

# -----------------------------------------------------------

def hacky_parse_for_library_title(html_string):
    classname_start = html_string.find("package-header__name")
    
    inner_start = html_string[classname_start:].find(">")
    text_start = inner_start + classname_start + 1
    
    inner_end = html_string[classname_start:].find("<")
    text_end = inner_end + classname_start
    
    return html_string[text_start:text_end].strip()

# -----------------------------------------------------------

def get_latest_version(library_name):
    '''
    Takes in library name as string, looks it up on pypi, and returns 
    current version number as string
    '''
    url = f"https://pypi.org/project/{library_name}/"
    try:
        result = request.urlopen(url)
        binary_data = result.read()
        data = binary_data.decode('utf-8')
        fulltitle = hacky_parse_for_library_title(data)
        try: 
            name, version = fulltitle.split(' ')
            return version
        except:
            raise WrongAssumptionError('get_latest_version',f"unable to split name and version properly. Full text is: \n{fulltext}")
            return None
    except:
        raise WrongAssumptionError('get_latest_version',f"unable to connect to {url}")
        return None

# -----------------------------------------------------------
# PROJECT SEARCH --------------------------------------------
# -----------------------------------------------------------

def get_libraries_and_versions_from_requirements(filepath):
    '''
    inputs: str:filepath for requirements.txt
    outputs: list of dicts {library : str:library_name, version : str:version_number}
    '''    
    libraries = []
    with open(filepath) as f:
        for line in f:
            line_text = str(line)
            if '#' in line_text:
                line_text = line_text.split('#')[0]
            if len(line_text) > 0: 
                if '==' in line_text:
                    library, version = line_text.split('==')
                elif '>=' in line_text or '>' in line_text:
                    library = line_text.split('>')[0]
                    version = None
                elif '<=' in line_text:
                    library, version = line_text.split('<=')
                elif '<' in line_text:
                    library, version = line_text.split('<')
                else:
                    library = line_text
                    version = None
                                
            if '[' in library:
                library = library.split('[')[0]
            libraries.append({'library':library,'version':version})
    return libraries

def check_file_for_library(filepath,library):
    '''
    inputs: str:filepath, str:library name
    outputs: list containing line #s (not counting 'import x') that the library is explicity in
    '''
    with open(filepath) as f:
        i = 0
        imported = False
        words_to_check = [library]
        affected_lines = []
        affected_lines_text = []
        for line in f:
            line_text = str(line)
            i += 1
            if 'import' in line_text and library in line_text:
                imported = True
                if '#' in line_text:
                    line_text = line_text.split('#')[0]
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
                            affected_lines_text.append(line_text)
                            words_to_check += check_line_for_new_variable(keyword,line_text)
                    elif keyword in line_text and i not in affected_lines:
                        affected_lines.append(i)
                        affected_lines_text.append(line_text)
                        words_to_check += check_line_for_new_variable(keyword,line_text)
    
    return {'linenums': affected_lines, 'linetext': affected_lines_text}

# -----------------------------------------------------------

def search_directory_for_library(directory,library):
    affected_files = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filepath = root + '/' + file
                    affected = check_file_for_library(filepath,library)
                    affected_lines = affected['linenums']
                    affected_lines_text = affected['linetext']
                    if len(affected_lines) > 0:
                        affected_files.append({'file':filepath,'lines':affected_lines,'linestext':affected_lines_text})
    except:
        raise WrongAssumptionError('search_directory_for_library',f"directory input '{directory}' is not valid directory path or is '{type(directory)}' type instead of str, bytes, or os.path object")
    return affected_files

# -----------------------------------------------------------

def check_file_for_imports(file):
    libraries = []
    with open(file) as f:
        for line in f:
            line_text = str(line)
            if 'import' in line_text:                   # this captures 'import x', 'import x as y', 'from x import a,b,c'
                libraries.append(line_text.split(' ')[1].strip())           # future: need to check for unusual import statements?
    return libraries

def search_directory_for_imports(dir_path):
    libraries = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                filepath = root + '/' + file
                try:
                    libraries += check_file_for_imports(filepath)
                except:
                    raise WrongAssumptionError('search_directory_for_imports',f"{filepath} not found in {os.listdir(dir_path)}")
    return libraries   

# -----------------------------------------------------------
# REPORT BUILDING -------------------------------------------
# -----------------------------------------------------------

def write_report_segment(directory,affected_by_outdated_library_dict,verbose):
    cutoff = len(directory) + 1
    report_segment = ""
    for affected in affected_by_outdated_library_dict:
        report_segment += f"\n\t{affected['file'][cutoff:]}"
        if verbose:
            for i in range(0,len(affected['lines'])):
                report_segment += f"\n\t\t{affected['lines'][i]:<10} | {affected['linestext'][i]}"
        else:
            report_segment += f"\n\t\t{affected['lines']}"
    return report_segment

# -----------------------------------------------------------

def write_report_segments_for_scales(scales_dict,affected_by_outdated_libraries,directory,verbose):
    report_segments = ''
    if len(scales_dict) > 0:
        for lib in scales_dict['libraries']:
            report_segments += f"\n[ ]{lib}"
            report_segments += write_report_segment(directory,affected_by_outdated_libraries[lib],verbose)
    else:
        report_segments += "\nNone"
        
    return report_segments


# -----------------------------------------------------------
# MAIN ------------------------------------------------------
# -----------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(description="Identify outdated libraries in your project dependencies and where they're used.")
    parser.add_argument('directory',action="store",help="Top level of project directory on which to run report.")
    parser.add_argument('-o','--out',action="store",help="Write thaw report file to specified file path; thaw will write timestamped .txt report file.")
    parser.add_argument('-v','--verbose',action="store_true",help="Include content of lines affected by out-of-date libraries (only line numbers will be written otherwise).")
    parser.add_argument('-l','--library',action="store",nargs='*',help="Search for instances of specified libraries instead of all outdated libraries.")
    parser.add_argument('-i','--imports',action="store_true",help="Check import statements in files instead of requirements.txt.")
    args = parser.parse_args()
    
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
    
    report_summary = ""
    report_body = ""
    
    if args.library and args.imports:
        print("--library and --imports flags cannot be used in the same report. Instead, please run thaw with one flag and then rerun with the other.")
    elif args.imports:
        libraries = search_directory_for_imports(args.directory)
        affected_by_libraries = {}
        libraries.sort()
        for lib in libraries:
            affected_by_libraries[lib] = search_directory_for_library(args.directory,lib)
            source = get_library_source(lib,args.directory)
            symbol = {'pypi':'*','local':'+','other':' '}
            report_summary += f"\t{symbol[source]}{lib:<40} | {len(affected_by_libraries[lib])} files affected\n"
            report_body += f"\n{lib}"
            report_body += write_report_segment(args.directory,affected_by_libraries[lib],args.verbose)
    elif args.library:
        affected_by_libraries = {}
        report_summary += '\n'
        for lib in args.library:
            affected_by_libraries[lib] = search_directory_for_library(args.directory,lib)
            report_summary += f"\t{lib:<40} | {len(affected_by_libraries[lib])} files affected\n"
            report_body += f"\n{lib}"
            report_body += write_report_segment(args.directory,affected_by_libraries[lib],args.verbose)
    else: 
        try:
            libraries = get_libraries_and_versions_from_requirements(os.path.join(args.directory,"requirements.txt"))
            affected_by_outdated_libraries = {}            
            for item in libraries:
                library = item['library']
                current_version = item['version']
                source = get_library_source(library,args.directory)
                if source == 'pypi':
                    latest_version = get_latest_version(library)
                else:
                    latest_version = None
                   
                if latest_version:
                    scale = version_update_scale(current_version,latest_version)
                    if scale:
                        scales[scale]["count"] += 1
                        scales[scale]["libraries"].append(library)
                        affected_by_outdated_libraries[library] = search_directory_for_library(args.directory,library)
                        version_change = current_version + ' >> ' + latest_version
                        report_summary += f"\t*{library:<40} | {version_change:<20} | {len(affected_by_outdated_libraries[library])} files affected\n"
                    else:
                        report_summary += f"\t{library:<41} | {current_version}, no update needed\n"
                major = scales['major']['count']
                minor = scales['minor']['count']
                micro = scales['micro']['count']
                report_body += f"{major + minor + micro} total updates: "
                report_body += f"{major} MAJOR updates, "
                report_body += f"{minor} MINOR updates, "
                report_body += f"{micro} MICRO updates\n"
                
                report_body += '\nMajor updates:'
                if len(scales['major']['libraries']) > 0:
                    for lib in scales['major']['libraries']:
                        report_body += f"\n[ ]{lib}"
                        report_body += write_report_segment(args.directory,affected_by_outdated_libraries[lib],args.verbose)
                else:
                    report_body += "\nNone"
                
                report_body += '\n\nMinor updates:'
                if len(scales['minor']['libraries']) > 0:
                    for lib in scales['minor']['libraries']:
                        report_body += f"\n[ ]{lib}"
                        report_body += write_report_segment(args.directory,affected_by_outdated_libraries[lib],args.verbose)            
                else: 
                    report_body += "\nNone"
                report_body += '\n\nMicro updates:'
                if len(scales['micro']['libraries']) > 0:
                    for lib in scales['micro']['libraries']:
                        report_body += f"\n[ ]{lib}"
                        report_body += write_report_segment(args.directory,affected_by_outdated_libraries[lib],args.verbose) 
            
            # with open(os.path.join(args.directory,"requirements.txt")) as requirements:
            #     affected_by_outdated_libraries = {}
 
            #     for line in requirements:
            #         if "==" in line:
            #             library, current_version = line.strip().split("==")
            #             if '[' in library:
            #                 library = library.split('[')[0]
            #             latest_version = get_latest_version(library)
            #             if latest_version:
            #                 scale = version_update_scale(current_version,latest_version)
            #                 if scale:
            #                     scales[scale]["count"] += 1
            #                     scales[scale]["libraries"].append(library)
            #                     affected_by_outdated_libraries[library] = search_directory_for_library(args.directory,library)
            #                     version_change = current_version + ' >> ' + latest_version
            #                     report_summary += f"\t*{library:<40} | {version_change:<20} | {len(affected_by_outdated_libraries[library])} files affected\n"
            #                 else:
            #                     report_summary += f"\t{library:<41} | {current_version}, no update needed\n"
            #         else:
            #             report_summary += f'\t{line.strip():<41} | no version requirement\n'

            #     major = scales['major']['count']
            #     minor = scales['minor']['count']
            #     micro = scales['micro']['count']
            #     report_body += f"{major + minor + micro} total updates: "
            #     report_body += f"{major} MAJOR updates, "
            #     report_body += f"{minor} MINOR updates, "
            #     report_body += f"{micro} MICRO updates\n"
                
            #     report_body += '\nMajor updates:'
            #     if len(scales['major']['libraries']) > 0:
            #         for lib in scales['major']['libraries']:
            #             report_body += f"\n[ ]{lib}"
            #             report_body += write_report_segment(args.directory,affected_by_outdated_libraries[lib],args.verbose)
            #     else:
            #         report_body += "\nNone"
                
            #     report_body += '\n\nMinor updates:'
            #     if len(scales['minor']['libraries']) > 0:
            #         for lib in scales['minor']['libraries']:
            #             report_body += f"\n[ ]{lib}"
            #             report_body += write_report_segment(args.directory,affected_by_outdated_libraries[lib],args.verbose)            
            #     else: 
            #         report_body += "\nNone"
            #     report_body += '\n\nMicro updates:'
            #     if len(scales['micro']['libraries']) > 0:
            #         for lib in scales['micro']['libraries']:
            #             report_body += f"\n[ ]{lib}"
            #             report_body += write_report_segment(args.directory,affected_by_outdated_libraries[lib],args.verbose) 
            
        except FileNotFoundError:
            print("No requirements file found - please run thaw in the top level of your project")
    
    if args.out:
        now = dt.now()
        report_title = f"thaw_report_{now.strftime('%m%d%y_%H%M%S')}.txt"
        report_filename = os.path.join(args.out,report_title)
        with open(report_filename,'w') as log:
            log.write(f"THAW REPORT RUN {now.strftime('%m/%d/%y %H:%M:%S')}")
            log.write('\n')
            log.write(report_summary)
            log.write('\n')
            log.write(report_body)
    print(report_summary)
    print('\n')
    print(report_body)
    print('\n')

    
if __name__ == "__main__":
    main()