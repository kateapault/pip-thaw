# THAW
Thaw is a tool that identifies outdated libraries in your requirements.txt file and generates a report file showing you exactly where updates would affect your project.

# Python 3 
Not compatible with Python 2

# Install:
```
$ pip install thaw
```

# Use:

Thaw must be run on the same level as your requirements.txt file (usually at the top level of your project).

To run:

```
$ thaw
``` 
This generates a report file, thaw_report.txt, at the same level that thaw was run.


# Info

Thaw was created because it's really frustrating to update to a newer library version and then fix errors one by one as they come up, especially if you're updating more than one library. Running thaw tells you which libraries are used where, including variables made with those libraries, so you can easily pinpoint where problems are if a library update breaks your project. 

✅  &nbsp; uses only built-in Python libraries - no dependencies to download

✅  &nbsp; checks requirements.txt for outdated versions

✅  &nbsp; identifies files in the project that use these outdated versions

✅  &nbsp; identifies lines in those files that use these outdated versions

✅  &nbsp; identifies variables in those files that are made with outdated library versions

✅  &nbsp; creates report file detailing which lines in which files would be affected by library updates


# Notes / planned additions:
- Explicitly distinguish between directly required libraries and dependencies
- Note dependency-affected lines as well as directly affected lines