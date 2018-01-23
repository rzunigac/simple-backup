# simple-backup

Simple backup script, you can backup a local mysql database and/or a folder. 

## Features
- Configure retention time for database and folder backup separately
- Deactivate backup of database or folder and just backup one of them
- Log file with comands executed and exceptions
- It uses standard python modules, no extra modules to install

## Usage
- Set the retention time of backups in days (ROTATE_DB_TIME, ROTATE_FOLDER_TIME)
- Set the database you want to backup (DB_BACKUP, HOST, DB_NAME, DB_USER, DB_PASSWORD) 
- Set the path to the folder you want to backup (CODE_BACKUP, CODE_FOLDER)

## Notes
- The script uses mysqldump and tar commands vis os.popen().
- The database backups are saved on a .sql file and the folder is compressed on a tar.gz file. Bot are on the backup subfolder.
- The script has a few comments that are in spanish but the names of the variables to edit are the ones mentioned on the usage section.
