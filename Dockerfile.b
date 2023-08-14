# Use the official uvicorn-gunicorn-fastapi image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Create a directory for the app and set it as the working directory
WORKDIR /app

# Copy the FastAPI application files into the container
COPY ./fastapi_test.py /app/fastapi_test.py
COPY ./database.py /app/database.py
COPY ./requirements.txt /app/requirements.txt
COPY ./tmp.db /app/tmp.db

# Install the required libraries
RUN pip install -r ./requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 80

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "fastapi_test:app", "--host", "0.0.0.0", "--port", "80"]

