from app import create_app
from app.config.settings import HOST, PORT, DEBUG

app, socketio = create_app()
# for development
if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG) 