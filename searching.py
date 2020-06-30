import os

def check_file_for_package(filename,package):
    '''
    inputs: str:filename, str:package (package name)
    outputs: list containing line #s (not counting imports) that the package is explicity in
    '''
    f = open(filename)
    i = 0
    imported = True
    affected_lines = []
    for line in f:
        i += 1
        # need to account for aliases 
        # and submodules
        # need to disregard comments
        # need to disregard if part of something eg 'cost' variable gets caught while looking for 'os' package
        if 'import' in line:
            imported = True
        elif imported and package in line:
            affected_lines.append(i)
    return affected_lines


dir_path = os.path.dirname(os.path.realpath(__file__))

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.py'):
            filepath = root + '/' + file
            affected_lines = check_file_for_package(filepath,'pyshorteners')
            if len(affected_lines) > 0:
                print(f"pyshorteners found on lines {affected_lines} in file {filepath}")

