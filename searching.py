import os

def check_package_name_isnt_subword(package,line):
    '''
    this assumes substring package has already been found inside string line
    returns True if package is indeed in line, False if not
    ex:
    check_package_name_isnt_subword('os','pathname = os.path.dirname("file")')
    >> True
    check_package_name_isnt_subword('os', 'total_cost = item_price + tax')
    >> False
    '''
    solo = True
    package_name_start_ind = line.find(package)
    package_name_end_ind = package_name_start_ind + len(package)
    if package_name_end_ind != len(line) - 1:
        if line[package_name_end + 1] not in '.()[]{} =#-+*/%':
            solo = False
    if line[package_name_start_ind - 1] not in '.()[]{} =/*+-%':
        solo = False
    return solo
    
    

def check_file_for_package(filename,package):
    '''
    inputs: str:filename, str:package (package name)
    outputs: list containing line #s (not counting 'import x') that the package is explicity in
    '''
    f = open(filename)
    i = 0
    imported = False
    affected_lines = []
    for line in f:
        line_text = str(line)
        i += 1
        # need to account for multiple submodules
        # need to disregard if part of something eg 'cost' variable gets caught while looking for 'os' package
        # Actually Useful and harder to code Mode: grab variables/etc made w package and identify lines using those
        if 'import' in line_text and package in line_text:
            imported = True
            if 'as' in line_text:
                package = line_text.split('as')[1].strip()
            elif 'from' in line_text:
                package = line_text.split('import')[1].strip()
        elif imported and '#' in line_text:
            if package in line_text.split('#')[0]:
                affected_lines.append(i)
        elif imported and package in line_text:
            affected_lines.append(i)
    return affected_lines

def search_directory_for_package(package='pyshorteners'):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    affected_files = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                filepath = root + '/' + file
                affected_lines = check_file_for_package(filepath,package)
                if len(affected_lines) > 0:
                    affected_files.append({'file':filepath,'lines':affected_lines})

    return affected_files

if __name__ == '__main__':
    print()
    print("PYSHORTENERS PACKAGE IS USED BY THE FOLLOWING FILES:")
    for f in search_directory_for_package():
        print(f"FILE: {f['file']}")
        print(f"LINES: {f['lines']}")
    