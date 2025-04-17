from binance.enums import *
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASES_DIR = os.path.join(BASE_DIR, 'databases')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
MarketDatabases = {
    'ETHUSDT':os.path.join(DATABASES_DIR, 'ETHUSDT_orders.sqlite'),
    'BTCUSDT':os.path.join(DATABASES_DIR, 'BTCUSDT_orders.sqlite'),
    'BTCUSDC':os.path.join(DATABASES_DIR, 'BTCUSDC_orders.sqlite'),
    'XRPUSDT':os.path.join(DATABASES_DIR, 'XRPUSDT_orders.sqlite'),
    'ADAUSDT':os.path.join(DATABASES_DIR, 'ADAUSDT_orders.sqlite'),
    'DOGEUSDT':os.path.join(DATABASES_DIR, 'DOGEUSDT_orders.sqlite'),
    'SOLUSDT':os.path.join(DATABASES_DIR, 'SOLUSDT_orders.sqlite'),
    'LTCUSDT':os.path.join(DATABASES_DIR, 'LTCUSDT_orders.sqlite')
    }

