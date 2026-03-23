import sys
import traceback

try:
    print("Starting API server test...")
    import api_server
    print("API server imported successfully")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
