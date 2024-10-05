FROM python:3.12.1-slim

# Clean apt and update package lists
RUN apt-get clean && rm -rf /var/lib/apt/lists/* && apt-get update --fix-missing \
    # Install curl and other required packages
    && apt-get install -y --no-install-recommends curl jq \
    # Set up Node.js (this installs Node.js from NodeSource)
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    # Install Netlify CLI using npm
    && npm install -g netlify-cli \
    # Clean up to reduce image size
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# add node-jq if needed
RUN npm install -g node-jq
