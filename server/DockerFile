# Use Python v3.11.8
FROM python:3.11.8 AS flask_builder

# Set working directory
WORKDIR /app

ADD requirements.txt run.py ./

# Install virtualenv
RUN pip install virtualenv

# Create and activate virtual environment
RUN python -m venv venv

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000
# Command to run Flask app
CMD ["python", "run.py"]
