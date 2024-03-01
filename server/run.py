from app import create_app

if __name__ == "__main__":
    # Run the Flask application in debug mode during development
    app = create_app("dev")
    app.run(host="0.0.0.0", debug=True)
