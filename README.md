# azure-functions-db
contains azure functions for db operations

## Pre-requisite:
Postgres-13
resources for azure function

Azure function:

After you have created the azure function container, ensure you add the following additional environment variables if not available.

[
  {
    "name": "AzureWebJobsStorage",
    "value": "connectionstring",
    "slotSetting": false
  },
  {
    "name": "DOCKER_CUSTOM_IMAGE_NAME",
    "value": "karthikkadajji1/azurefunction",
    "slotSetting": false
  },
  {
    "name": "DOCKER_ENABLE_CI",
    "value": "true",
    "slotSetting": false
  },
  {
    "name": "FUNCTION_APP_EDIT_MODE",
    "value": "readOnly",
    "slotSetting": false
  },
  {
    "name": "FUNCTIONS_EXTENSION_VERSION",
    "value": "~4",
    "slotSetting": false
  },
  {
    "name": "MACHINEKEY_DecryptionKey",
    "value": "your decryptkey",
    "slotSetting": false
  },
  {
    "name": "PGHOST",
    "value": <your host name of postgres>,
    "slotSetting": false
  },
  {
    "name": "PGPASSWORD",
    "value": <postgres password>,
    "slotSetting": false
  },
  {
    "name": "PGUSER",
    "value": <postgres user>,
    "slotSetting": false
  },
  {
    "name": "STORAGE_CONNECTION_STRING",
    "value": <storage string for database>,
    "slotSetting": false
  },
  {
    "name": "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING",
    "value": <your connection string>,
    "slotSetting": false
  },
  {
    "name": "WEBSITE_CONTENTSHARE",
    "value": "your key",
    "slotSetting": false
  },
  {
    "name": "WEBSITES_ENABLE_APP_SERVICE_STORAGE",
    "value": "false",
    "slotSetting": false
  }
]
  
 Configure your azure app to pull from the image using
 NOTE: it is advisible to build your own image and push it to docker hub and add the webhook to enable cicd
  
  ## building the image:
  
  docker build --tag <dockerid>/tag .
  docker push <dockerid>/tag
  
  ####To run locally
  docker run -p 8080:80 -it <dockerid>/tag bash 
  
Testing endpoint in azure:
https://<appname>/api/databasebackup?code=<function code>/&database_name=<db name>&container_name=<container name>
