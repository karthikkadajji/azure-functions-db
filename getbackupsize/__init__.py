import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.storage.filedatalake import DataLakeServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    container_name = req.params.get('container_name')
    database_name = req.params.get('database_name')
    service_client = DataLakeServiceClient.from_connection_string(os.getenv('STORAGE_CONNECTION_STRING'))
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv('STORAGE_CONNECTION_STRING'))

    try:
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        paths = file_system_client.get_paths(path=database_name)
        num_of_backups = 0
        total_size_of_backups = 0
        for blob in paths:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob)
            if blob_client.get_blob_properties().size :
                total_size_of_backups += blob_client.get_blob_properties().size
                num_of_backups += 1
        logging.info(f"Number of backups for {database_name}: {num_of_backups}")
        logging.info(f"Total size of backups {database_name}: {total_size_of_backups}")
        return func.HttpResponse(f"Hello {num_of_backups}, {total_size_of_backups}!")
    except Exception as e:
        return func.HttpResponse(f"Error: {e} while getting the size, count of the backups for {database_name}")