from flask_socketio import emit
from app.services.stock_service import CryptoService
from app.config.settings import PRICE_UPDATE_INTERVAL
import time
import threading
import random
from datetime import datetime, timedelta

class WebSocketHandler:
    def __init__(self):
        self.clients = set()
        self.crypto_service = CryptoService()
        self.subscriptions = {}
        self.polling_thread = None
        self.is_polling = False
        self.socketio = None
        self.last_prices = {
            'bitcoin': 65000,
            'ethereum': 3500
        }
        sample_data = self.crypto_service.sample_data
        self.current_timestamp = self._get_last_timestamp(sample_data)
        self.update_count = 0

    def _get_last_timestamp(self, sample_data):
        try:
            bitcoin_data = sample_data['historical']['bitcoin']['prices']
            last_ts = int(bitcoin_data[-1][0])
            return last_ts
        except:
            now = datetime.now()
            return int(now.timestamp() * 1000)

    def _generate_price_update(self, symbol):
        current_price = self.last_prices[symbol]
        change_percent = random.uniform(-0.5, 0.5)
        new_price = current_price * (1 + change_percent / 100)
        self.last_prices[symbol] = new_price
        
        self.update_count += 1
        new_timestamp = self.current_timestamp + (self.update_count * PRICE_UPDATE_INTERVAL * 1000)
        
        return {
            'symbol': symbol,
            'price': round(new_price, 2),
            'timestamp': new_timestamp
        }

    def handle_connect(self, sid, socketio=None):
        if socketio:
            self.socketio = socketio
            
        self.clients.add(sid)
        self.subscriptions[sid] = []
        print(f"Client connected: {sid}")
        
        self.update_count = 0
        
        if not self.is_polling:
            self.start_polling()

    def handle_disconnect(self, sid):
        try:
            if sid in self.clients:
                self.clients.remove(sid)
            if sid in self.subscriptions:
                del self.subscriptions[sid]
            print(f"Client disconnected: {sid}")
            
            if not self.clients:
                self.stop_polling()
                self.update_count = 0
        except Exception as e:
            print(f"Error in disconnect handler: {e}")

    def handle_subscribe(self, coin_ids, sid):
        try:
            if isinstance(coin_ids, str):
                coin_ids = [coin_ids]
            
            self.subscriptions[sid] = coin_ids
            self.update_count = 0
            
            for coin_id in coin_ids:
                if coin_id in self.last_prices:
                    update = self._generate_price_update(coin_id)
                    if self.socketio:
                        self.socketio.emit('price_update', update, room=sid)
        except Exception as e:
            print(f"Error in subscribe handler: {e}")

    def start_polling(self):
        if not self.socketio:
            print("Warning: No SocketIO instance available for polling")
            return
            
        self.is_polling = True
        self.polling_thread = threading.Thread(target=self._poll_prices)
        self.polling_thread.daemon = True
        self.polling_thread.start()

    def stop_polling(self):
        self.is_polling = False
        if self.polling_thread:
            self.polling_thread.join()
            self.polling_thread = None

    def _poll_prices(self):
        while self.is_polling:
            try:
                all_coins = set()
                for coins in self.subscriptions.values():
                    all_coins.update(coins)
                
                if all_coins and self.socketio:
                    for sid, subscribed_coins in self.subscriptions.items():
                        for coin_id in subscribed_coins:
                            if coin_id in self.last_prices:
                                update = self._generate_price_update(coin_id)
                                print(f"Sending update: {update}")
                                self.socketio.emit('price_update', update, room=sid)
            except Exception as e:
                print(f"Error in price polling: {e}")
            
            time.sleep(PRICE_UPDATE_INTERVAL)

    def send_price_updates(self, default_symbols, socketio):
        try:
            self.socketio = socketio
            all_coins = set()
            for coins in self.subscriptions.values():
                all_coins.update(coins)
            
            if not all_coins:
                all_coins.update(default_symbols)
            
            if all_coins:
                for sid, subscribed_coins in self.subscriptions.items():
                    for coin_id in all_coins:
                        if (coin_id in subscribed_coins or not subscribed_coins) and coin_id in self.last_prices:
                            update = self._generate_price_update(coin_id)
                            print(f"Sending update: {update}")
                            self.socketio.emit('price_update', update, room=sid)
        except Exception as e:
            print(f"Error in price polling: {e}")

websocket_handler = WebSocketHandler() 