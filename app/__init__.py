from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_swagger_ui import get_swaggerui_blueprint
import threading
from app.config.settings import (
    DEBUG, HOST, PORT, CORS_ORIGINS, SWAGGER_URL, 
    API_URL, SWAGGER_CONFIG, SOCKET_CORS_ORIGINS,
    UPDATE_INTERVAL, DEFAULT_SYMBOLS
)
from app.api.routes import api
from app.api.swagger import get_swagger_spec
from app.api.websocket import websocket_handler

def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    
    CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})
    
    # Configure SocketIO
    socketio = SocketIO(app, 
                       cors_allowed_origins=SOCKET_CORS_ORIGINS,
                       ping_timeout=10,
                       ping_interval=5,
                       async_mode='threading')
    
    # Configure Swagger 
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config=SWAGGER_CONFIG
    )
    
    # Register blueprints
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(api, url_prefix='/api')
    
    @app.route("/static/swagger.json")
    def swagger_spec():
        return get_swagger_spec()
    
    # Configure WebSocket events
    @socketio.on('connect')
    def handle_connect():
        print(f"Client connecting with SID: {request.sid}")
        websocket_handler.handle_connect(request.sid, socketio)

    @socketio.on('disconnect')
    def handle_disconnect(data=None):
        print(f"Client disconnecting with SID: {request.sid}")
        websocket_handler.handle_disconnect(request.sid)

    @socketio.on('subscribe')
    def handle_subscribe(symbols):
        print(f"Client {request.sid} subscribing to: {symbols}")
        websocket_handler.handle_subscribe(symbols, request.sid)
    
    @socketio.on_error()
    def error_handler(e):
        print(f"SocketIO error: {e}")
        
    @socketio.on_error_default
    def default_error_handler(e):
        print(f"SocketIO default error: {e}")
    
    def price_update_thread():
        while True:
            try:
                with app.app_context():
                    websocket_handler.send_price_updates(DEFAULT_SYMBOLS, socketio)
                socketio.sleep(UPDATE_INTERVAL)
            except Exception as e:
                print(f"Error in price update thread: {e}")
                socketio.sleep(5)
    
    if not DEBUG:
        thread = threading.Thread(target=price_update_thread)
        thread.daemon = True
        thread.start()
    
    return app, socketio 