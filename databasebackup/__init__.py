import azure.functions as func
import subprocess
import os
from datetime import datetime
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient
from pathlib import Path
import logging


def dump_database(database_name):
    password = os.getenv('PGPASSWORD')
    host_name = os.getenv('PGHOST')
    user_name = os.getenv('PGUSER')
    pattern = 'cron.job*'

    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = database_name + str(time_stamp) + ".dump"

    database_bck_path = os.path.join("/tmp", backup_file)

    command = f'pg_dump -Fc -v --host={host_name} --username={user_name} --dbname={database_name} -T {pattern} -f {database_bck_path}'
    try:
        proc = subprocess.Popen(command, shell=True, env={
            'PGPASSWORD': password
        })
        proc.wait()
    except Exception as e:
        logging.error(f"Error {e} while running the backup of {database_name}")
    return database_bck_path


def upload_backup_container(container_name, upload_file_path):
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv('STORAGE_CONNECTION_STRING'))
    new_container = blob_service_client
    try:
        new_container = blob_service_client.create_container(container_name)
    except ResourceExistsError:
        pass
    blob_client = new_container.get_blob_client(
        container=container_name, blob=Path(upload_file_path).name)
    try:
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data, blob_type="BlockBlob")
        logging.info(
            f"Uploaded backup to {container_name} as blob {Path(upload_file_path).name}")
    except Exception as error:
        logging.error(f"Error: {error} while uploading the file ")
    finally:
        os.remove(upload_file_path)


def main(req: func.HttpRequest) -> func.HttpResponse:
    database_name = req.params.get("database_name")
    container_name = req.params.get("container_name")
    backup_path = ""
    try:
        backup_path = dump_database(database_name=database_name)
        upload_backup_container(container_name, backup_path)
        return func.HttpResponse(f"Uploaded backup to {container_name} as blob {Path(backup_path).name}")
    except Exception as e:
        logging.error(f"Error {e} while running the backup of {database_name}")
        return func.HttpResponse(f"Error {e} while running the backup of {database_name}")
