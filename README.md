FastAPI Scraper Application
===========================
This is a FastAPI application that scrapes a website and stores the data in a postgres database. The application uses a redis cache to store the scraped data. The application also uses a proxy server to scrape the website.

Prerequisites
-------------
Add env_local.py file
---------------------
Create a file named `env_local.py` in the root directory of the project. Add the following code to the file:
```json
{
  "APP_HOST": "0.0.0.0",
  "APP_PORT": 3000,
  "BASE_URL": "https://dentalstall.com/shop",
  "DB_URL": "postgresql+asyncpg://postgres:postgres@localhost:5432/scraper",
  "REQUEST_RETRIES": 3,
  "REDIS_HOST": "localhost:6379",
  "AUTH_TOKEN": "Random123"
}
```

To set up PostgreSQL, Redis, and run migrations for the first time, execute the following commands for MAC:
```bash
chmod +x setup.sh
./setup.sh
```


Build and Run the Application
-----------------------------
To start the server, run:

```bash
python3 main.py
```

Running the API
---------------
You can use the following cURL command to test the API:
```bash
curl --location --request GET 'http://0.0.0.0:3000/api/v1/scrape' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer Random123' \
--data '{
  "page_limit": 1,
  "proxy": ""
}'
```

OR 

Alternatively, you can use the Swagger documentation to interact with the API. Access it at: http://0.0.0.0:3000/docs


Removing keys from Redis
------------------------
To check the keys in Redis, run the following command:
```bash
redis-cli --scan --pattern "http*"
```
To remove keys from Redis, run the following command:
```bash
redis-cli --scan --pattern "http*" | while read key; do redis-cli del "$key"; done
```
