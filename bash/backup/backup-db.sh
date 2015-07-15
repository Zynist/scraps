#!/bin/bash
#
# Backs up a single file (e.g. sqlite database) to another local directory and then Google Drive
# Keeps a log of backups and saves any errors to be reported by email to the administrator

#--------------------
# Applications
DRIVE=/path/to/gdrive/app/drive # GDrive sync app at https://github.com/rakyll/drive
CP=/bin/cp
DATE=`/bin/date +%Y%m%d%H%M%S`

# Directories
DATADIR= # source of backup data
BACKUPDIR= # local backup destination dir
GDRIVEDIR= # local Google Drive sync directory 

# Files
BACKUPFILE=filename ## Name of file to backup here - e.g. sqlite.db
BACKUPNAME=$DATE-$BACKUPFILE # name of backup - date prepended

# Other
LOGFILE=/path/to/log/file.log
ADMINEMAIL=administrator@example.org
SERVERNAME=MyAppBackup # Application or server name for email
#--------------------

catch_errors(){
  exit_code=$?
  echo "Backup script failed: $(date)" >> $LOGFILE
  cat stderr.log >> $LOGFILE
  echo -e "Backup failed at $(date) on $(hostname).\n-----\nError Log:\n$(cat stderr.log)" | mail -s "[$SERVERNAME] Backup Failure" $ADMINEMAIL
  exit $exit_code
}

trap catch_errors ERR;

echo "---------------------------------" >> $LOGFILE
echo "Backup Started." >> $LOGFILE
$CP $DATADIR/app.db $BACKUPDIR/$BACKUPNAME 2> >(tee stderr.log >&2)
echo "Backup successful: $(date)" >> $LOGFILE

$CP $BACKUPDIR/$BACKUPNAME $GDRIVEDIR/ 2> >(tee stderr.log >&2)
yes | $DRIVE push $GDRIVEDIR 2> >(tee stderr.log >&2)
echo "Google Drive sync successful: $(date)" >> $LOGFILE
if [ -f stderr.log ];
then
   rm stderr.log
fi
