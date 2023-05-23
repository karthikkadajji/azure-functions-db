#!/bin/bash
STORAGE_NAME="testsfasdfsd"
APP_NAME="testappasdfasdf"
DOCKER_IMAGE="karthikkadajji1/azurefunction:azurefunctions1"
az functionapp plan create --resource-group AzureFunctionsContainers-rg --name myPremiumPlan --location eastus --number-of-workers 1 --sku EP1 --is-linux
az functionapp create --name $APP_NAME --storage-account $STORAGE_NAME --resource-group AzureFunctionsContainers-rg --plan myPremiumPlan --image $DOCKER_IMAGE --runtime python
# $conn = $(az storage account show-connection-string --resource-group AzureFunctionsContainers-rg --name $STORAGE_NAME --query connectionString)
# az functionapp config appsettings set --name $APP_NAME --resource-group AzureFunctionsContainers-rg --settings AzureWebJobsStorage=$conn
az functionapp create --name testappasdfasdf --storage-account testsfasdfsd --resource-group AzureFunctionsContainers-rg --plan myPremiumPlan --deployment-container-image-name karthikkadajji1/azurefunction --runtime python --functions-version 4
az functionapp deployment container config --enable-cd --query CI_CD_URL --output tsv --name testappasdfasdf --resource-group AzureFunctionsContainers-rg
