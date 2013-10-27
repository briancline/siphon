#!/bin/bash
## This file is what's retrieved and parsed by siphon to check whether it
## needs to transfer down any new files.
##
## This is ideal to throw into a */5 minute crontab on the remote.


LOCK_FILE=.siphon.lock

[ -f $LOCK_FILE ] && exit 1
echo 1 > $LOCK_FILE

SOURCE_DIR=complete
SUMS_FILE=files.txt

if [ ! -f $SUMS_FILE ]; then
    touch -t 200101010000.00 $SUMS_FILE
fi

find $SOURCE_DIR -type f -newer $SUMS_FILE -print0 \
    | xargs -0 -I{} \
    md5sum "{}" >> $SUMS_FILE

rm -f $LOCK_FILE
