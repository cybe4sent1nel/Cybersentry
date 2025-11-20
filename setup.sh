# File: setup.sh
#!/bin/bash

# Upgrade pip and install core external dependencies from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Manually install the local project as an editable package.
# This ensures that all internal imports (like 'from cybersentry.sdk.agents import...')
# are correctly resolved by the Python interpreter inside the cloud environment.
pip install -e .
