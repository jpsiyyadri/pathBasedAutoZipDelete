from zipfile import ZipFile
import os
import pathlib
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename='{}_logs.log'.format(datetime.now().strftime("%d_%m_%Y")), format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG,filemode='a')
AUDIT_FILE_CONTENTS = []

def delete_files(file_names=[]):
    for fyle in file_names:
        if os.path.exists(fyle):
            os.remove(fyle)
        else:
            print("*** The file does not exist ***")

def create_zip_file(file_names=[]):
    if(len(file_names)):
        # create a ZipFile object
        zipObj = ZipFile('sample.zip', 'w')
        # Add multiple files to the zip
        for fyle in file_names:
            zipObj.write(fyle)
        # close the Zip File˝
        zipObj.close()
    else:
        print("**** No files are here to zip ****")

def prepare_zip_files():
    try:
        with open("backup.txt", "r") as f:
            txt = f.readlines()
            files_to_zip = []
            for t in txt:
                extracted_path = t.strip().split('|')
                if(len(extracted_path)>0):
                    fname = pathlib.Path(extracted_path[1])
                    retention_period = int(extracted_path[2])
                    AUDIT_FILE_CONTENTS.append({
                        "file_name": extracted_path[1],
                        "retention_period": retention_period
                    })
                    assert fname.exists(), f'No such file: {fname}'
                    # check if the file older than the days mentioned
                    logging.info("# check if the file older than the days mentioned")                    
                    file_created_time = datetime.fromtimestamp(fname.stat().st_mtime)
                    if(datetime.today() - timedelta(days=retention_period) >=  file_created_time):
                        files_to_zip.append(extracted_path[1])
    
            create_zip_file(files_to_zip)
    finally:
        f.close()

def prepare_delete_files():
    try:
        with open("purge.txt", "r") as f:
            txt = f.readlines()
            files_to_delete = []
            for t in txt:
                extracted_path = t.strip().split('|')
                if(len(extracted_path)>0):
                    fname = pathlib.Path(extracted_path[1])
                    retention_period = int(extracted_path[2])
                    AUDIT_FILE_CONTENTS.append({
                        "file_name": extracted_path[1],
                        "retention_period": retention_period
                    })
                    assert fname.exists(), f'No such file: {fname}'
                    # check if the file older than the days mentioned
                    logging.info("# check if the file older than the days mentioned")
                    file_created_time = datetime.fromtimestamp(fname.stat().st_mtime)
                    if(datetime.today() - timedelta(days=retention_period) >= file_created_time):
                        files_to_delete.append(extracted_path[1])
            delete_files(files_to_delete)
            logging.info("File successfully purged")
    finally:
        f.close()

def write_into_audit_file():
    audit_file_name = '{}_audit.txt'.format(datetime.now().strftime("%d_%m_%Y"))
    try:
        with open(audit_file_name, 'w') as f:
            for itm in AUDIT_FILE_CONTENTS:
                f.write("{0} {1}\n".format(itm['file_name'], itm['retention_period']))
    finally:
        f.close()


if __name__=="__main__":
    # zip files
    prepare_zip_files()
    # delete files
    prepare_delete_files()
    # audit file
    write_into_audit_file()
