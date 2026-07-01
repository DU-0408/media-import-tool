#!/usr/bin/env bash

set -e

echo "Installing Media Import Tool..."

# Check for python3
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found. Please install it."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate and install requirements
echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Create wrapper script
echo "Creating wrapper script 'import-media'..."
cat << 'EOF' > import-media
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
sudo "${SCRIPT_DIR}/venv/bin/python" "${SCRIPT_DIR}/main.py" "$@"
EOF

chmod +x import-media

echo "Installation complete!"
echo ""
echo "To use the tool, you can run:"
echo "  ./import-media"
echo ""
echo "Note: The wrapper script automatically uses sudo, as it is required to set permissions in /mnt directories."
