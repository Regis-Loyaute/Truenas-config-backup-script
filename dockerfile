FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the script file and set the CMD instruction
COPY truenas-backup.py .
CMD ["python3", "truenas-backup.py"]
