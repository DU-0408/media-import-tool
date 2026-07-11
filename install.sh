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

# Resolve symlink to find the true directory of this script
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

# Intercept update command
if [ "$1" == "update" ]; then
    echo "Updating Media Import Tool..."
    cd "$SCRIPT_DIR" || exit 1
    git pull
    "${SCRIPT_DIR}/venv/bin/pip" install -r requirements.txt
    echo -e "\nUpdate complete! 🎉"
    exit 0
fi

sudo "${SCRIPT_DIR}/venv/bin/python" "${SCRIPT_DIR}/main.py" "$@"
EOF

chmod +x import-media

echo "Installing globally to /usr/local/bin/import-media (requires sudo)..."
sudo ln -sf "$(pwd)/import-media" /usr/local/bin/import-media

echo "Installation complete!"
echo ""
echo "You can now run the tool from anywhere by simply typing:"
echo "  import-media"
echo ""
echo "To quickly update the tool and dependencies in the future, run:"
echo "  import-media update"
