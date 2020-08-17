# THAW
Thaw is a tool that identifies outdated libraries in your requirements.txt file and generates a report file showing you exactly where updates would affect your project.


# Install:
```
$ pip install thaw
```

# Use:
```
$ python3 thaw.py
``` 
This generates a report file, thaw_report.txt, at the same level that thaw was run.

# Info

✅  &nbsp; uses only built-in Python libraries - no dependencies to download

✅  &nbsp; checks requirements.txt for outdated versions

✅  &nbsp; identifies files in the project that use these outdated versions

✅  &nbsp; identifies lines in those files that use these outdated versions

✅  &nbsp; identifies variables in those files that are made with outdated versions

✅  &nbsp; creates report file detailing which lines in which files would be affected by selected updates

# Notes:


# Planned additions / fixes:
- Reformat the report file to make it easier to read
- Explicitly distinguish between directly required libraries and dependencies
- Note which lines dependencies affect (at the moment thaw only identifies directly used libraries)

