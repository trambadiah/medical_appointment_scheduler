FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
# We do this before copying the rest of the app to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that FastAPI runs on
EXPOSE 8000

# Set the working directory to the backend folder 
# so that python imports (like 'from api.chat import...') work correctly
WORKDIR /app/backend

# Command to run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
