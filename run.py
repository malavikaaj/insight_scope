"""
Main script to run the InsightScope application.
"""
import os
import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent))

def run_streamlit():
    """Run the Streamlit frontend."""
    os.system("streamlit run insight_scope/app/frontend/app.py")

def process_data(directory=None, file=None):
    """Process data files."""
    from insight_scope.app.api.data_ingestion import DataIngestionPipeline
    
    pipeline = DataIngestionPipeline()
    
    if directory:
        print(f"Processing directory: {directory}")
        results = pipeline.process_directory(directory)
    elif file:
        print(f"Processing file: {file}")
        results = pipeline.process_file(file)
    else:
        print("Processing default data directory")
        from insight_scope.config.config import RAW_DATA_DIR
        results = pipeline.process_directory(str(RAW_DATA_DIR))
    
    print("Processing results:")
    for result in results if isinstance(results, list) else [results]:
        print(f"- {result['file']}: {result['status']}")
        if result['status'] == 'success':
            print(f"  Chunks: {result.get('chunks', 'N/A')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="InsightScope - Enterprise Knowledge Assistant")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Streamlit command
    streamlit_parser = subparsers.add_parser("run", help="Run the Streamlit frontend")
    
    # Process data command
    process_parser = subparsers.add_parser("process", help="Process and index documents")
    process_parser.add_argument("--dir", help="Directory containing documents to process")
    process_parser.add_argument("--file", help="Single file to process")
    
    args = parser.parse_args()
    
    if args.command == "run" or not args.command:
        run_streamlit()
    elif args.command == "process":
        process_data(args.dir, args.file)
    else:
        parser.print_help()