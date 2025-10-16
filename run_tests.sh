#!/bin/bash
# Test runner script for Mergington High School Activities API

echo "🧪 Running FastAPI Tests for Mergington High School Activities..."
echo "================================================="

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v

echo ""
echo "✅ Test run complete!"
echo "📊 Coverage report generated in htmlcov/ directory"
echo "🎯 Goal: All tests should be passing with high coverage"