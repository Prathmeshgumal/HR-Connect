#!/bin/bash

echo "🚀 Setting up Resume Upload System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully!"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install React dependencies
echo "📦 Installing React dependencies..."
cd frontend
npm install

if [ $? -eq 0 ]; then
    echo "✅ React dependencies installed successfully!"
else
    echo "❌ Failed to install React dependencies"
    exit 1
fi

cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Create a .env file with your Supabase credentials"
echo "2. Start the backend: python app.py"
echo "3. Start the frontend: cd frontend && npm start"
echo ""
echo "🌐 The app will be available at:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:5000"
echo ""
echo "📖 For detailed instructions, see README.md" 