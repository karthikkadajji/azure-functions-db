# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.8-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.8

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true
# RUN apt-get update && apt-get install -y lsb-release && echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
# CMD wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
# RUN gpg --keyserver pgpkeys.mit.edu --recv-key  7FCC7D46ACCC4CF8 && gpg -a --export 7FCC7D46ACCC4CF8 |  apt-key add -
# ENV DEBIAN_FRONTEND noninteractive
# ENV DEBCONF_NOWARNINGS="yes"
RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot