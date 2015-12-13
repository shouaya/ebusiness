
#backup -> save eb database backup file
#download -> save hr database backup file
#database -> save eb&hr ddl
#log -> do.sh output log file

#config.sh -> hr and eb database connection settings
		   -> batch folder path
		   
#Authorize user run the shell
-> chmod 777 batch/*

#run backup
-> ./back.sh

#run download
-> ./download.sh

#run restore
-> ./restore

#run all
-> ./do.sh