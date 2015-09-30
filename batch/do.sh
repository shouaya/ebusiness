#!/bin/bash
# 機能  :  sync hr datatables to eb
# 作成  :  shoushou
source /usr/local/src/ebusiness/batch/config.sh

current_date=$(date "+%Y.%m.%d")
LOGFILE=$EB_ROOT/log/$current_date.log.txt


current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "backup start : $current_time" >> $LOGFILE
.$EB_ROOT/backup.sh

if [ "$?" -eq 0 ]
then
  echo 'backup success' >> $LOGFILE
else
  echo 'backup error' >> $LOGFILE
  exit
fi

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "download start : $current_time" >> $LOGFILE
.$EB_ROOT/download.sh

if [ "$?" -eq 0 ]
then
  echo 'download success' >> $LOGFILE
else
  echo 'download error' >> $LOGFILE
  exit
fi

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "restore start : $current_time" >> $LOGFILE
.$EB_ROOT/restore.sh

if [ "$?" -eq 0 ]
then
  echo 'restore success' >> $LOGFILE
else
  echo 'restore error' >> $LOGFILE
  exit
fi