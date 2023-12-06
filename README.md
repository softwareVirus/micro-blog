# Project Name

Brief description of Flask project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/softwareVirus/micro-blog
    cd micro-blog
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    .venv/bin/activate  # On Windows
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Create a `.env` file in the root of your project with the following content:

    ```env
    MONGODB_CONNECTION_STRING=your_mongodb_connection_string
    ```

   Replace `your_mongodb_connection_string` with your actual MongoDB connection string.

2. Run the Flask application:

    ```bash
    flask --app ./app/app.py run
    ```

