#!/bin/sh
#
# pre-commit hook to check if new .py files has licence-header.

if git rev-parse --verify HEAD >/dev/null 2>&1
then
    against=HEAD
else
    # Initial commit: diff against an empty tree object
    against=$(git hash-object -t tree /dev/null)
fi


# Redirect output to stderr.
exec 1>&2

# Retrieve the list of newly added files
newly_added_files=($(git diff --name-only --diff-filter=A --cached))
if [ -n "$newly_added_files" ]
then
    # Check for Copyright statement
    for newly_added_file in $newly_added_files; do
        if [[ $newly_added_file =~ \.py$ ]];
        then
            files_without_header+=($(grep -L "Licensed under the Apache License" $newly_added_file))
        fi
    done

    if [ -n "$files_without_header" ]
    then
        echo "License header not found in the following newly added files:"
        for file in "${files_without_header[@]}"
        do
            :
            echo "   - $file";
        done
        exit 1;
    else
        exit 0;
        fi
fi


# If there are whitespace errors, print the offending file names and fail.
exec git diff-index --check --cached $against --