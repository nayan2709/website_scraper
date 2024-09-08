#!/bin/bash

# Install Homebrew if not installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew already installed."
fi

# Update Homebrew
echo "Updating Homebrew..."
brew update

# Install PostgreSQL
if ! brew list postgresql &> /dev/null
then
    echo "Installing PostgreSQL..."
    brew install postgresql
else
    echo "PostgreSQL is already installed."
fi

# Start PostgreSQL service
echo "Starting PostgreSQL service..."
brew services start postgresql

# Install Redis
if ! brew list redis &> /dev/null
then
    echo "Installing Redis..."
    brew install redis
else
    echo "Redis is already installed."
fi

# Start Redis service
echo "Starting Redis service..."
brew services start redis


# PostgreSQL setup
echo "Setting up PostgreSQL..."

PG_DB="scraper"
PG_USER="postgres"

# Check if the postgres user exists
if ! psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${PG_USER}'" | grep -q 1; then
    echo "Creating PostgreSQL user ${PG_USER}..."
    createuser -s ${PG_USER}
else
    echo "PostgreSQL user ${PG_USER} already exists."
fi

# Check if the database exists
if ! psql -U "${PG_USER}" -tAc "SELECT 1 FROM pg_database WHERE datname='${PG_DB}'" | grep -q 1; then
    echo "Creating database ${PG_DB}..."
    createdb -O "${PG_USER}" ${PG_DB}
else
    echo "Database ${PG_DB} already exists."
fi

# Set environment variables for Alembic
export DATABASE_URL="postgresql+psycopg2://@localhost/${PG_DB}"

# Install Python requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head


echo "Setup completed successfully."


