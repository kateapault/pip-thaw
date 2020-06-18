
"""
pip-thaw updates versions in your requirements.txt file that are out of date.

You can choose to apply all changes or select from major/minor/micro.

Requires ``pip`` Version 9 or higher!

Installation::
    pip install pip-thaw

Usage::
    pip-thaw -h
    
    --f --files             lists files that will have errors?
    --u --update            takes arguments minor/major/micro/all, can take multiple
    OR -----------> 
    --a --all               apply all updates
    --j --major             apply major updates
    --n --minor             apply minor updates
    --c --micro             apply micro updates
    --mr --major-minor      apply major and minor updates
    --mi --minor-micro      apply minor and micro updates
"""
import argparse
from datetime import datetime as dt
import subprocess
import sys

from pypi_search import get_latest_version

# --------------------------------------------
# SETTINGS -----------------------------------
# --------------------------------------------

logfile = "thaw_log.txt"

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


def version_change_scale(old_version_string, new_version_string):
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
    
    
# --------------------------------------------
# MAIN ---------------------------------------
# --------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="An update helper")
    
    try:
        requirements = open("requirements.txt")
    except FileNotFoundError:
        print("No requirements file found - please run thaw in the top level of your project")
    
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
    
    log = open(logfile,"a+")
     
    report_time = f"pip-thaw {dt.now().strftime('%m-%d-%y %H:%M:%S')}\n"
    report_body = ""
    
    for line in requirements:

        if "==" in line:
            library, current_version = line.strip().split("==")
            latest_version = get_latest_version(library)
            scale = version_change_scale(current_version,latest_version)
            if scale:
                scales[scale]["count"] += 1
                report_body += f"\t*{library:<40} | {current_version} >> {latest_version}\n"
            else:
                report_body += f"\t{library:<41} | {current_version}\n"
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
    
if __name__ == "__main__":
    main()