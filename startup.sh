#!/bin/bash
# Function to check if the network link is up
check_network_status() {
    ping -c 1 google.com > /dev/null 2>&1
    return $?
}

# Wait for the network link to be up
while ! check_network_status; do
    echo "Waiting for network link to be up..."
    sleep 5  # Adjust the sleep interval as needed
done

# Continue with the rest of your script
echo "Network link is up, continuing with the script."

cd /home/bmg/Desktop/LightShot-Screenshots-Scraper/
echo "Creating poetry"
poetry shell
echo "Installing dependencies"
poetry install
echo "Running program"
python3 main.py
