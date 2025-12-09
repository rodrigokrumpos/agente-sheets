
from sheets_handler import append_to_sheet
import logging

# Setup basic logging to see output
logging.basicConfig(level=logging.INFO)

print("--- Starting Verification ---")

dummy_data = {
    'nome': 'TEST_USER_VERIFICATION',
    'whatsapp': '5511999999999',
    'empreendimento': 'TEST_PROJECT_VERIFICATION'
}

try:
    print(f"Appending data: {dummy_data}")
    append_to_sheet(dummy_data)
    print("--- Append Successful! Check your Google Sheet ---")
except Exception as e:
    print(f"--- FAILED: {e} ---")
