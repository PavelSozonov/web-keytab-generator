#!/bin/sh

# TODO: Stub script, need to be changed to ktutil as follow
# printf "%b" "addent -password -p ${USER} -k 1 -e aes256-cts\n${PASSWORD}\nwkt ${USER}.keytab" | ktutil

USER=$1
PASSWORD=$2
FILENAME=$3

touch ${FILENAME}
echo ${USER} > ${FILENAME}
echo ${PASSWORD} >> ${FILENAME}
