# BizGPT Project
This is BizGPT hiring project

## I. Prerequisite
1. First install `Google chrome` and `chromedriver` so we can crawl dynamic sites. You can download the latest versions in this site:  
`https://googlechromelabs.github.io/chrome-for-testing/`
2. Then make a virtual environment and change the environment to the new environment
```
python3 -m venv env && source env/bin/activate
```
1. Now install the requirements with this command:  
```
pip3 -r install < requirements.txt
```
1. You should setup your postgres database. you can achieve this with this command:  
```
sudo docker run \
--name BizGPT \
-e POSTGRES_PASSWORD=12345 \  
-e POSTGRES_USER=admin \  
-e POSTGRES_DB=qavanin \  
-p 5432:5432 \  
postgres
``` 

## II. 