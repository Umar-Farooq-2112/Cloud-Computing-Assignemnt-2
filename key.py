from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Path to your service account key JSON file
key_path = "key.json"

# Load the credentials
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Refresh and obtain the token
credentials.refresh(Request())
auth_token = credentials.token

print("Your OAuth 2.0 Token:", auth_token)
