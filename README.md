# BizGPT Project
This is BizGPT project. 

## Overview
This project has four main part:  
1. DB: for intracting with database and reading and writing to it
2. Embedding: for setup the ML model and get embedding of text from it
3. QavaningCrawler: this is the crawler for crawling the Qavanin.ir website.  
4. main: this is for building a simple api to intract with the service (using fastapi)

### API
Our API has only one endpint for searching and finding the results that have most similarity to our sentence. You can try and test it with this endpoint `localhost:8000/docs`
* endpoint: `localhost:8000/search`
* input: `q: this is the query you want to search`  
* output: `results: a json response that is like this{"url": score}` note that the output is sorted by score meaning the most similar results is on the top


## How to run?
In This section We discuss how to make environment, install dependancies and required packages and running the project.
### I. Prerequisites
1. First install `Google chrome` and `chromedriver` so we can crawl dynamic sites. You can download the latest versions in this site:  
`https://googlechromelabs.github.io/chrome-for-testing/`
2. Then make a virtual environment and change the environment to the new environment
```
python3 -m venv env && source env/bin/activate
```
3. Now install the requirements with this command:  
```
pip3 -r install < requirements.txt
```
4. You should setup your postgres database. you can achieve this with this command:  
```
sudo docker run \
--name BizGPT \
-e POSTGRES_PASSWORD=12345 \  
-e POSTGRES_USER=admin \  
-e POSTGRES_DB=qavanin \  
-p 5432:5432 \  
postgres
``` 
5. make an .env file like .env-sample

### II. Executing
Run the server using this command:  
```
fastapi dev main.py
```