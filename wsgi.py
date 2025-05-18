from app import create_app

app, socketio = create_app()

# for production
if __name__ == "__main__":
    socketio.run(app) 