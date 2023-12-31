# Use the official uvicorn-gunicorn-fastapi image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Create a directory for the app and set it as the working directory
WORKDIR /app

# Copy the FastAPI application files into the container
COPY ./fastapi_test.py /app/fastapi_test.py
COPY ./database.py /app/database.py
COPY ./requirements.txt /app/requirements.txt
COPY ./tmp.db /app/tmp.db
COPY ./app.py /app/app.py

# Install the required libraries
RUN pip install -r ./requirements.txt

# Expose the ports
EXPOSE 8501 8000

# Run the Streamlit and FastAPI apps using uvicorn
CMD ["sh", "-c", "streamlit run app.py & uvicorn fastapi_test:app --host 0.0.0.0 --port 8000"]
