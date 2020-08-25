# thaw 

![PyPI](https://img.shields.io/pypi/v/thaw?color=purple) [![Coverage Status](https://coveralls.io/repos/github/kateapault/pip-thaw/badge.svg?branch=master)](https://coveralls.io/github/kateapault/pip-thaw?branch=master) ![GitHub issues](https://img.shields.io/github/issues/kateapault/pip-thaw) ![PyPI - License](https://img.shields.io/pypi/l/thaw) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/thaw)


**thaw** is a command line tool that identifies precisely where project dependencies are used. It is designed to help with CI and with general project updates by providing a roadmap of where dependency updates would impact your project.

By default thaw looks at the project's ```requirements.txt``` file, and there are also options to search for dependencies based on import statements or to only report where specific libraries are used. 

[See planned features and progress here.](https://github.com/users/kateapault/projects/1)

**Requires Python 3. Not compatible with Python 2. Tested with Python 3.7/3.8**



## Installation
You can install thaw with pip and PyPI:
```
$ pip3 install thaw
```

## Use
thaw takes one positional argument, the root/top level of your project directory. 

Running thaw with its default settings will look through your ```requirements.txt``` file and print a report of where they're used to stdout:

```
$ python3 -m thaw .
``` 

You can write the report to a .txt file with the ```--out``` flag. This creates a timestamped file in the location you specify:
```
python3 -m thaw . ---out /put/report/here
```

By default, the report will have filepaths relative to the project's root directory and line numbers for each affected file. You can have the report include the line content by using the ```--verbose``` flag:
```
python3 -m thaw . --verbose
```

If you have no ```requirements.txt``` file or if you want to get a report on where all dependencies are used, use the ```--imports``` flag:
```
python3 -m thaw . --imports
```

Alternatively, if you want to search for one or several libraries in particular, use the ```--library``` flag and enter the names of the libraries separated by spaces:
```
python3 -m thaw . --library pandas numpy
```

## Example report
```
	*library1                                 | 2.9 >> 2.10          | 2 files affected
	*library2                                 | 3.8 >> 4.0           | 1 files affected
	library3                                  | 4.9.1, no update needed
	library4                                  | no version number listed

2 total updates: 1 MAJOR updates, 1 MINOR updates, 0 MICRO updates

Major updates:
[ ]library2
	file3.py
		[19, 22, 23, 28, 47, 49]
    file4.py
        [6, 12, 13, 14, 110, 212, 213]

Minor updates:
[ ]library1
    file1.py
		[14, 15, 16, 22, 87, 88, 209, 211, 212]
    file2.py
        [16, 18, 21]
    file3.py
        [24, 89, 134, 137]

Micro updates:
none

```

## Bugs/Requests
Please use the [GitHub issue tracker](https://github.com/kateapault/pip-thaw/issues) to submit bugs or request features. 

You can check planned features on thaw's [GitHub project board](https://github.com/users/kateapault/projects/1).

## Background

thaw was created because it's super frustrating to update project dependencies and then play whack-a-mole with errors. The report thaw generates tells you which libraries are used where, including variables made with those libraries, so you can easily pinpoint where problems may occur and have a roadmap for fixing update-induced errors. 