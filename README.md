# THAW
Thaw is a tool that identifies outdated libraries in your requirements.txt file and generates a report file showing you exactly where updates would affect your project.

# Python 3 
Not compatible with Python 2

# Install:
```
$ pip install thaw
```

# Run:

Thaw *must* be run on the same level as your requirements.txt file (usually at the top level of your project).

```
$ python -m thaw
``` 
or
```
$ python3 -m thaw
```
This generates a report file, thaw_report.txt, at the same level that thaw was run.

# Use Cases
Thaw is helpful for CI and for updating project dependencies.


# Info

Thaw was created because it's super frustrating to update libraries for a project and then cycle through running your project and fixing a single error at a time. Thaw tells you which libraries are used where, including variables made with those libraries, so you can easily pinpoint where problems may occur and have a roadmap for fixing update-induced errors.

✅  &nbsp; Thaw uses only built-in Python libraries - no dependencies to download

✅  &nbsp; Thaw checks requirements.txt for outdated versions and then searches your entire project

✅  &nbsp; Thaw identifies files in the project that use these outdated versions

✅  &nbsp; Thaw identifies which lines in those files use these outdated versions

✅  &nbsp; Thaw identifies any variables in those files that are made with outdated library versions

✅  &nbsp; Thaw creates a report file, thaw_report.txt, detailing all of that information


# Notes / planned additions:
- Explicitly distinguish between directly required libraries and dependencies
- Note dependency-affected lines as well as directly affected lines