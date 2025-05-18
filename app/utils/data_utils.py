from datetime import datetime
from typing import Dict, List, Any
from app.config.settings import VS_CURRENCY

def format_kline_data(prices: List, volumes: List, market_caps: List, coin_info: Dict) -> List[Dict]:
    formatted_data = []
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
            kline_data.update(get_coin_extra_info(coin_info))

        formatted_data.append(kline_data)

    return formatted_data

def get_coin_extra_info(coin_info: Dict) -> Dict[str, Any]:
    return {
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
    } 