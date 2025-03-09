# Use a RHEL UBI 8 base image
FROM registry.access.redhat.com/ubi8/python-39

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install system dependencies
RUN dnf -y install postgresql-libs

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the OPC UA port
EXPOSE 4840

# Run the OPC UA server
CMD ["python", "opcua_server.py"]
