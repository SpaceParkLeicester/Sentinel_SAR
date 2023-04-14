# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /home/vardh/gcp_project/oiltanks/

# Setting venv
ENV VIRTUAL_ENV=/opt/env
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the requirements file into the container and install the dependencies
COPY requirements.txt ./
RUN pip install -v --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/home/vardh/gcp_project/oiltanks"

# Set the entrypoint to the Python file you want to run
ENTRYPOINT ["pytest", "oil_storage_tanks/tests/data/test_auth.py"]