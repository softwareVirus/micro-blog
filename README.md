# Micro-blog

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/softwareVirus/micro-blog
    cd micro-blog
    ```

2. Go  to server directory
    ```bash
    cd server
    ```

3. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    ./venv/Script/activate  # On Windows
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. After that, create new terminal and go to ./your-path/micro-blog/client directory
    
    ```bash
    npm install
    ```
## Usage
### Server
1. Go to server directory

    ```bash
    cd server
    ```

2. Create a `.env` file in the server directory of your project with the following content:

    ```env
    MONGODB_CONNECTION_STRING=your_mongodb_connection_string
    ```

   Replace `your_mongodb_connection_string` with your actual MongoDB connection string.

3. Run the Flask application:

    ```bash
    flask --app ./app/app.py run
    ```
### Client
1. Run the Vue application:

    ```bash
    cd client
    npm run serve
    ```

