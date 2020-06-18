
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
import subprocess
import sys

from pypi_search import get_latest_version

# --------------------------------------------
# SETTINGS -----------------------------------
# --------------------------------------------

pip_cmd = "pip3"

check_cmd = "pip3 list --local --outdated"

# err = sys.stderr.write
# out = sys.stdout.write


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
    
    # cmd_list = check_cmd.split(' ')
    
    # process = subprocess.Popen(cmd_list,
    #                            stdout=subprocess.PIPE,
    #                            stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    # outdated_versions_dict = dictify_pip_list(stdout)

    # commented_requirements_text = ""
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
    for line in requirements:

        if "==" in line:
            library, current_version = line.strip().split("==")
            latest_version = get_latest_version(library)
            scale = version_change_scale(current_version,latest_version)
            if scale:
                scales[scale]["count"] += 1
            # print(f"{library:<20} | {scale} | {current_version:<10} | {latest_version:<10}")

        # if current_version != latest_version:
        #     printline = f"{library} - {outdated_versions_dict[library]['scale']} update required"
        #     print(printline)
        #     latest = outdated_versions_dict[library]["latest"]
        #     if len(line) <= 50:
        #         new_commented_line = f"{line.strip():<50}\t#{latest}\n"
        #     else:
        #         new_commented_line = f"{line.strip()}\t#{latest}\n"
        #     commented_requirements_text += new_commented_line
        # elif line.strip() != "-e .":
        #     commented_requirements_text += line
    print(f"{scales['major']['count'] + scales['minor']['count'] + scales['micro']['count']} TOTAL updates")
    print(f"{scales['major']['count']} MAJOR updates")
    print(f"{scales['minor']['count']} MINOR updates")
    print(f"{scales['micro']['count']} MICRO updates")
    requirements.close()

    # requirements = open("requirements.txt","w")
    # requirements.write(commented_requirements_text)
    # requirements.close()
    
if __name__ == "__main__":
    main()