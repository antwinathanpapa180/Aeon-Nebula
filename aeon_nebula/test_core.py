from core import NeuralCore
import os
from dotenv import load_dotenv

print("--- MANUALLY TESTING NEURAL CORE INITIALIZATION ---")
load_dotenv(override=True)
print(f"URL loaded from env: {os.environ.get('SUPABASE_URL')}")

try:
    core = NeuralCore()
    print("✅ SUCCESS: NeuralCore initialized perfectly!")
    print(f"Database Online Status: {core.is_cloud_online()}")
except Exception as e:
    print("❌ FAILURE: Core crashed during initialization.")
    print(f"Error Message: {e}")