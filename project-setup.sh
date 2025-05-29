#!/bin/bash
mkdir "my portfolio"
cd "my portfolio" 
# Create subdirectories
mkdir controllers models views static database tests logs

# Create base files
touch app.py requirements.txt .gitignore README.md .env logging_config.py

# Initialize Git repository
git init

# Print success message
echo "✅ Project structure created successfully!"
