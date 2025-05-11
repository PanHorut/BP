# Server part
**Author:** Dominik Horut (`xhorut01`)

## Server development setup

### 1. Install dependencies
```sh
pip install -r requirements.txt
```

### 2. Environment setup
Before running the application, ensure that the database has already been created. To seed the database, use the `.sql` file located in the `db_init` directory.

Next, configure the required environment variables in your `.env` file:

```sh
DJANGO_SETTINGS_MODULE=be.settings
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=YOUR_PASSWORD
MYSQLDATABASE=YOUR_DATABASE_NAME
MYSQLPORT=YOUR_PORT
```

Additionally, the application uses **Azure Speech-to-Text** and **Gemini** services. To authenticate these services, add your respective API keys to the `.env` file:
```sh
AZURE_API_KEY=YOUR_AZURE_API_KEY
AZURE_REGION=YOUR_AZURE_REGION
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 3. Run database migrations
```sh
python manage.py migrate
```

### 4. Start the Server with Uvicorn
```sh
uvicorn be.asgi:application --host 0.0.0.0 --port 8000 --reload
```