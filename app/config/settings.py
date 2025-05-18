from datetime import datetime, timedelta

# Flask settings
DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

CORS_ORIGINS = "*"

DEFAULT_SYMBOLS = ['bitcoin', 'ethereum', 'binancecoin', 'ripple', 'cardano']

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
SWAGGER_CONFIG = {
    'app_name': "Crypto Trading API"
}

SOCKET_CORS_ORIGINS = "*"
UPDATE_INTERVAL = 2  

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
PRICE_UPDATE_INTERVAL = 1  
VS_CURRENCY = "usd"  

MAX_HISTORICAL_DAYS = 365  

# Default parameters
DEFAULT_END_DATE = datetime.now().strftime('%Y-%m-%d')
DEFAULT_START_DATE = (datetime.now() - timedelta(days=MAX_HISTORICAL_DAYS-1)).strftime('%Y-%m-%d')  # Last 364 days
DEFAULT_SYMBOL = 'bitcoin'
DEFAULT_INTERVAL = 'daily' 