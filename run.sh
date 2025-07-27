#!/bin/bash

# Adobe India Hackathon 2025 - Round 1A Run Script (Heuristic Only)

set -e

echo "Starting Adobe India Hackathon 2025 - Round 1B Solution"
echo "================================================================================="

# Check system resources
echo "System Resources:"
echo "- CPU cores: $(nproc)"
echo "- Memory: $(free -h | grep 'Mem:' | awk '{print $2}' 2>/dev/null || echo 'N/A')"
echo "- Platform: $(uname -m)"

# Set environment variables
export PYTHONPATH=/app/src
export OMP_NUM_THREADS=4

# Check input directory
if [ ! -d "/app/input" ]; then
    echo "Error: Input directory /app/input not found"
    exit 1
fi

# Count PDF files
PDF_COUNT=$(find /app/input -name "*.pdf" -o -name "*.PDF" 2>/dev/null | wc -l)
echo "Found $PDF_COUNT PDF files to process"

# Check if output directory exists
if [ ! -d "/app/output" ]; then
    echo "Error: Output directory /app/output not found"
    exit 1
fi




echo "================================================================================="
echo "Starting persona-driven analysis..."
python /app/main.py


echo "======================================================"
echo "Processing complete! Results available in /app/output/"


# Check results
OUTPUT_COUNT=$(find /app/output -name "*.json" 2>/dev/null | wc -l)
echo "Generated $OUTPUT_COUNT JSON output files"