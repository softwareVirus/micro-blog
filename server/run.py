from app.socket import socketio, app
if __name__ == "__main__":
    # Run the Flask application in debug mode during development
    socketio.run(app, host="0.0.0.0", debug=True)

