#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Script para generar respaldos de una carpeta y una base de datos.

Es posible configurar el tiempo de retención de los respaldos en el 
sistema de archivos, la ruta de la carpeta y la base de datos mysql 
(por ahora).

 TO-DO:
 - Soporte para Multiples folder y database
 - Soporte para configurar postgresql o mysql
 - Archivo de configuracion externo
 - PEP compliance? hahaha
 
Creado: 06/06/2015
"""

__author__ = "Rodrigo Zuñiga Cuevas"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "rzunigac@gmail.com"
__status__ = "Production"

import logging
import os
import sys
import time

### CUANTOS DIAS PASAN ANTES DE BORRAR LOS RESPALDOS
ROTATE_DB_TIME = 30
ROTATE_FOLDER_TIME = 2

### DONDE ESTA EL CODIGO A RESPALDAR
CODE_BACKUP = True
CODE_FOLDER = os.path.normpath('/path/to/app/folder')

### BASE DE DATOS A RESPALDAR
DB_BACKUP = True
HOST = 'localhost'
DB_NAME='nutshell'
DB_USER = 'root'
DB_PASSWORD = '123456'

### Variables Globales
### DONDE SE GUARDAN LOS RESPALDOS
CURRENT_DIRECTORY = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FOLDER = CURRENT_DIRECTORY+'/backup'
filestamp = time.strftime('%Y-%m-%d-%I_%M')


def main():
    logpath = CURRENT_DIRECTORY + '/log/' + sys.argv[0].split('/')[-1].split('.')[0] + '.log'
    logging.basicConfig(filename=logpath, level=logging.DEBUG, format='[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

def db_dump():
    try:
        output_file = OUTPUT_FOLDER +'/'+ DB_NAME+"_"+filestamp+".sql"

        cmd = "mysqldump -u %s -p%s -h %s -e --opt -c %s --result-file %s" % (DB_USER, DB_PASSWORD, HOST, DB_NAME, output_file)
        os.popen(cmd)
        logging.info(cmd)
    except Exception as e:
        logging.exception("Error en funcion db_dump()")
        logging.exception(e)

def code_backup():
    try:
        output_file = OUTPUT_FOLDER+'/'+os.path.basename(CODE_FOLDER)+"_"+filestamp+'.tar.gz'
        os.popen("tar -czf %s %s" % (output_file, CODE_FOLDER))
        logging.info("tar -czf %s %s" % (output_file, CODE_FOLDER))
    except Exception as e:
        logging.exception("Error en funcion code_backup()")
        logging.exception(e)

def clean():
    try:
        CUT_FOLDER_TIME = time.time() - (ROTATE_FOLDER_TIME * 86400)
        CUT_DB_TIME = time.time() - (ROTATE_DB_TIME * 86400)

        files = os.listdir(OUTPUT_FOLDER)
        for filename in files:
            if '.tar.gz' in filename:
#                print "FOLDER"
                CUT_TIME = CUT_FOLDER_TIME
            elif '.sql' in filename:
#                print "DATABASE"
                CUT_TIME = CUT_DB_TIME
            else:
#                print "OTRO"
                continue
            f = os.path.join(OUTPUT_FOLDER, filename)
            if os.path.isfile(f) and os.stat(f).st_mtime < CUT_TIME:
#                print "Borrando "+ f+": "+time.ctime(os.stat(f).st_mtime)
                logging.info("Borrando "+ f+": "+time.ctime(os.stat(f).st_mtime))
                os.remove(f)
    except Exception as e:
        logging.exception("Error en funcion clean()")
        logging.exception(e)

if __name__ == "__main__":
    main()    
    if DB_BACKUP == True:
        db_dump()
    if CODE_BACKUP == True:
        code_backup()        
    clean()
    

