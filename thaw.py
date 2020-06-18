
"""
pip-thaw updates versions in your requirements.txt file that are out of date.

You can choose to apply major changes (eg v1.x -> v2.x), minor changes (eg v1.0 -> v1.3), or all changes.

Requires ``pip`` Version 9 or higher!

Installation::
    pip install pip-thaw

Usage::
    pip-thaw -h
"""
import argparse
import subprocess
import sys


# --------------------------------------------
# SETTINGS -----------------------------------
# --------------------------------------------

pip_cmd = "pip3"

check_cmd = "pip3 list --outdated"

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
    
    cmd_list = check_cmd.split(' ')
    # print(f"cmd_list: {cmd_list}")
    process = subprocess.Popen(cmd_list,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    outdated_versions_dict = dictify_pip_list(stdout)
    
    # print(outdated_versions_dict)

    commented_requirements_text = ""
    
    for line in requirements:
        library = line.split("==")[0]
        if library in outdated_versions_dict:
            printline = f"{library} - {outdated_versions_dict[library]['scale']} update required"
            print(printline)
            latest = outdated_versions_dict[library]["latest"]
            if len(line) <= 50:
                new_commented_line = f"{line.strip():<50}\t#{latest}\n"
            else:
                new_commented_line = f"{line.strip()}\t#{latest}\n"
            commented_requirements_text += new_commented_line
        elif line.strip() != "-e .":
            commented_requirements_text += line
            
    requirements.close()

    requirements = open("requirements.txt","w")
    requirements.write(commented_requirements_text)
    requirements.close()
    
if __name__ == "__main__":
    main()