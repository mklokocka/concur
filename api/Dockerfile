# Python runtimes.
FROM python:3-slim

# Working directory.
WORKDIR /api

# Add requirements.
COPY requirements.txt /api

# Install required libraries.
RUN pip --no-cache-dir install -r requirements.txt

# Add source.
COPY app.py /api

# Expose port 8080.
EXPOSE 8080

# Run the application.
CMD ["python", "app.py"]