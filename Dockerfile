# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

# Switch to the non-root user
USER appuser

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt /app/requirements.txt

# Switch to root to install packages
USER root

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Switch back to the non-root user
USER appuser

# Copy the rest of the application files
COPY main.py /app/main.py
COPY templates /app/templates
COPY ktutil.sh /app/ktutil.sh
COPY static /app/static

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "info"]
