# Use the official Telegraf image as the base
FROM telegraf:latest

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for our custom scripts
RUN mkdir -p /opt/scripts

# Copy the Python script and requirements
COPY src/parse_modem_status.py /opt/scripts/
COPY src/requirements.txt /opt/scripts/

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r /opt/scripts/requirements.txt

# Make the script executable
RUN chmod +x /opt/scripts/parse_modem_status.py

# The default command will still be telegraf, but now with our script available
CMD ["telegraf"]
