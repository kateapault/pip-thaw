# thaw
Package update tool that:

✅  uses only built-in Python libraries - no dependencies to download

✅  checks requirements.txt for outdated versions

✅  identifies files in the project that use these outdated versions

✅  identifies lines in those files that use these outdated versions

✅  identifies variables in those files that are made with outdated versions

✅  creates report file detailing which lines in which files would be affected by selected updates

# Install:
```$ pip install thaw```

# Use:
```$ thaw``` to generate a report file (thaw_report.txt)

# Notes:
The report file is pretty ugly right now and it doesn't distinguish between directly required libraries and dependencies. 

Report file should note primary/secondary package, ~~should break packages up into minor/major/micro categories,~~ ?should include simple list of packages that don't need updates?, should be much better formatted (possibly as checklist)
