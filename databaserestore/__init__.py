import logging
import os
import azure.functions as func
import subprocess
from azure.storage.blob import BlobServiceClient

def restore_database(database_name, backup_file_path):
    """Restore a database backup using pg_restore"""

    password = os.getenv('PGPASSWORD')
    host_name = os.getenv('PGHOST')
    user_name = os.getenv('PGUSER')
    try:
        pg_restore_command = [
            f'pg_restore --dbname={database_name} --host={host_name} --username={user_name} --no-owner --no-password {backup_file_path}'
        ]
        proc = subprocess.Popen(pg_restore_command, shell=True, env={
            'PGPASSWORD': password
        })
        # Execute the pg_restore command using subprocess
        proc.wait()
        logging.info("Database backup restored successfully.")
    except Exception as e:
        logging.error(f"Error restoring database backup: {e}")
        return func.HttpResponse(f"Error restoring database backup: {e}")

def download_backup_container(container_name, blob):
    """Download a blob from a container"""

    download_file_path = os.path.join("/tmp", blob)
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv('STORAGE_CONNECTION_STRING'))
    blob_client = blob_service_client.get_blob_client(container = container_name, blob = blob)
        
    try:
        with open(file=download_file_path, mode="wb") as download_file:
            download_stream = blob_client.download_blob()
            download_file.write(download_stream.readall())
        return download_file_path
    except Exception as error:
        logging.error(f"Error: {error} while downloading the file {blob}")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request to do a database restore.')
    restore_db = req.params.get('restore_db')
    container_name = req.params.get('container_name')
    download_file_path = download_backup_container(container_name=container_name, blob = "student120230523121538.dump")
    restore_database(restore_db, download_file_path)
    return func.HttpResponse(f"Database {restore_db} restored successfully.")


