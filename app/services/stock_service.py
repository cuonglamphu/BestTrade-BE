from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import json
import os
from app.config.settings import (
    VS_CURRENCY, 
    MAX_HISTORICAL_DAYS, DEFAULT_START_DATE
)
import time

class CryptoService:
    def __init__(self):
        self.sample_data = self._load_sample_data()

    def _load_sample_data(self) -> Dict:
        """Load sample data from JSON file"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.json')
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading sample data: {e}")
            return {}

    def get_crypto_price(self, coin_id: str) -> float:
        """Get current cryptocurrency price"""
        try:
            if coin_id in self.sample_data:
                return float(self.sample_data[coin_id]['market_data']['current_price']['usd'])
            return 0
        except Exception as e:
            print(f"Error getting crypto price for {coin_id}: {e}")
            return 0

    def get_symbols_data(self, coin_ids: List[str]) -> List[Dict[str, str]]:
        """Get data for multiple cryptocurrencies"""
        try:
            symbols_data = []
            for coin_id in coin_ids:
                if coin_id in self.sample_data:
                    symbols_data.append({
                        "symbol": coin_id,
                        "price": str(self.sample_data[coin_id]['market_data']['current_price']['usd'])
                    })
            return symbols_data
        except Exception as e:
            print(f"Error getting symbols data: {e}")
            return []

    def validate_date_range(self, start_date: str, end_date: str) -> Tuple[str, str, str]:
        """Validate and adjust date range based on API limitations"""
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            today = datetime.now()

            # check date
            if end_dt > today:
                end_dt = today
                end_date = end_dt.strftime('%Y-%m-%d')

            date_range = (end_dt - start_dt).days

            if date_range > MAX_HISTORICAL_DAYS:
                start_dt = end_dt - timedelta(days=MAX_HISTORICAL_DAYS-1)
                start_date = start_dt.strftime('%Y-%m-%d')
                message = f"Date range exceeded maximum allowed ({MAX_HISTORICAL_DAYS} days). Adjusted to last {MAX_HISTORICAL_DAYS} days."
            else:
                message = ""

            return start_date, end_date, message

        except ValueError as e:
            print(f"Error validating dates: {e}")
            return DEFAULT_START_DATE, end_date, "Invalid date format. Using default date range."

    def get_historical_data(self, coin_id: str, start_date: str, end_date: str, interval: str = 'daily') -> Dict[str, Any]:
        """Get historical data for a cryptocurrency"""
        try:
            start_date, end_date, message = self.validate_date_range(start_date, end_date)

            # get data
            if coin_id not in self.sample_data.get('historical', {}):
                return {
                    'data': [],
                    'info': {
                        'start_date': start_date,
                        'end_date': end_date,
                        'error': f"No historical data available for {coin_id}"
                    }
                }

            market_data = self.sample_data['historical'][coin_id]
            coin_info = self.sample_data[coin_id]

            formatted_data = []
            if not market_data.get('prices'):
                return {
                    'data': [],
                    'info': {
                        'start_date': start_date,
                        'end_date': end_date,
                        'error': "No price data available"
                    }
                }
            
            prices = market_data['prices']
            volumes = market_data.get('total_volumes', [])
            market_caps = market_data.get('market_caps', [])

            prices_len = len(prices)
            volumes_len = len(volumes)
            market_caps_len = len(market_caps)

            for i in range(prices_len):
                timestamp = int(prices[i][0] / 1000) 
                price = prices[i][1]
                volume = volumes[i][1] if i < volumes_len else 0
                market_cap = market_caps[i][1] if i < market_caps_len else 0

                prev_price = prices[i-1][1] if i > 0 else price
                change = price - prev_price
                change_percent = (change / prev_price * 100) if prev_price > 0 else 0

                kline_data = {
                    'time': timestamp,
                    'trading_date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
                    'price': float(price),
                    'volume': float(volume),
                    'market_cap': float(market_cap),
                    'change': float(change),
                    'change_percent': float(change_percent)
                }

              
                if i == prices_len - 1:
                    kline_data.update({
                        'name': coin_info.get('name', ''),
                        'symbol': coin_info.get('symbol', '').upper(),
                        'market_cap_rank': coin_info.get('market_cap_rank', 0),
                        'total_supply': float(coin_info.get('market_data', {}).get('total_supply', 0) or 0),
                        'max_supply': float(coin_info.get('market_data', {}).get('max_supply', 0) or 0),
                        'circulating_supply': float(coin_info.get('market_data', {}).get('circulating_supply', 0) or 0),
                        'ath': float(coin_info.get('market_data', {}).get('ath', {}).get(VS_CURRENCY, 0) or 0),
                        'atl': float(coin_info.get('market_data', {}).get('atl', {}).get(VS_CURRENCY, 0) or 0),
                        'ath_change_percentage': float(coin_info.get('market_data', {}).get('ath_change_percentage', {}).get(VS_CURRENCY, 0) or 0),
                        'atl_change_percentage': float(coin_info.get('market_data', {}).get('atl_change_percentage', {}).get(VS_CURRENCY, 0) or 0)
                    })

                formatted_data.append(kline_data)

            return {
                'data': formatted_data,
                'info': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'message': message if message else None
                }
            }
        except Exception as e:
            print(f"Error getting historical data for {coin_id}: {e}")
            return {
                'data': [],
                'info': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'error': str(e)
                }
            } 