from flask import Blueprint, jsonify, request
from app.services.stock_service import CryptoService
from app.config.settings import DEFAULT_SYMBOLS, DEFAULT_SYMBOL, DEFAULT_START_DATE, DEFAULT_END_DATE, DEFAULT_INTERVAL

api = Blueprint('api', __name__)
crypto_service = CryptoService()

@api.route('/')
def root():
    return jsonify({"message": "Welcome to Cryptocurrency Market API"})

@api.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@api.route('/symbols')
def get_symbols():
    try:
        symbols_data = crypto_service.get_symbols_data(DEFAULT_SYMBOLS)
        return jsonify(symbols_data)
    except Exception as e:
        print(f"Error in get_symbols: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('/klines')
def get_klines():
    try:
        coin_id = request.args.get('symbol', DEFAULT_SYMBOL)
        interval = request.args.get('interval', DEFAULT_INTERVAL)
        start_date = request.args.get('start_date', DEFAULT_START_DATE)
        end_date = request.args.get('end_date', DEFAULT_END_DATE)
        
        result = crypto_service.get_historical_data(
            coin_id=coin_id,
            start_date=start_date,
            end_date=end_date,
            interval=interval
        )
        
        if result.get('info', {}).get('error'):
            return jsonify({
                'error': result['info']['error'],
                'info': result['info']
            }), 400
            
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_klines for {coin_id}: {e}")
        return jsonify({"error": str(e)}), 500 