#!/bin/bash

function executeCommand () {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "Error with $1" >&2
    else echo "DONE"
    fi
    return $status
}

echo "NOTE: The local db password is 'careertalk'"

echo "Creating the \"careertalk\" database"
executeCommand createdb -h localhost careertalk -O careertalk -U careertalk

echo "Creating the \"careertalk-test\" database"
executeCommand createdb -h localhost careertalk-test -O careertalk -U careertalk
