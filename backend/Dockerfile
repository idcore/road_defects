# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy your application files into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port your application runs on (e.g., 5000 for Flask)
EXPOSE 5000

# Command to run your application
CMD ["python", "main.py"]