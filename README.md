# vcxproj cleaner

Apparently, Visual Studio has no option to clean up bad references from the solution (ie. files that were deleted from the filesystem but no excluded from the project). You have to manually check each file and exclude it from the solution or manually edit the `vcxproj` files.
 
This script checks the `vcxproj` files for include lines that reference deleted/renamed files and deletes them.

## How to run

Make a backup of `.vcxproj` and `.vcxproj.filters` files first.

```python vcxproj-cleaner.py "path/to/vcxproj-files"```

## Additional Notes

Microsoft, please put Code in you Visual Studio.