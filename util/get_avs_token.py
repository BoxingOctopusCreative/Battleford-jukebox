import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
from urllib.parse import parse_qs, urlparse
from config import (
    AVS_CLIENT_ID, 
    AVS_CLIENT_SECRET
)

REDIRECT_URI = "http://localhost:3000/callback"

# Store the authorization code
auth_code = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query_components = parse_qs(urlparse(self.path).query)
        
        if 'code' in query_components:
            auth_code = query_components['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this window.")
        
        # Stop the server
        self.server.server_close()

def get_refresh_token():
    # Start local server
    server = HTTPServer(('localhost', 3000), CallbackHandler)
    
    # Construct authorization URL
    auth_url = (
        "https://www.amazon.com/ap/oa"
        f"?client_id={AVS_CLIENT_ID}"
        "&scope=alexa:all"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
    )
    
    # Open browser for user authorization
    webbrowser.open(auth_url)
    
    # Wait for callback
    server.handle_request()
    
    if not auth_code:
        raise Exception("Failed to get authorization code")
    
    # Exchange authorization code for refresh token
    token_url = "https://api.amazon.com/auth/o2/token"
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": AVS_CLIENT_ID,
        "client_secret": AVS_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to get refresh token: {response.text}")
    
    return response.json()["refresh_token"]

if __name__ == "__main__":
    try:
        refresh_token = get_refresh_token()
        print(f"\nYour refresh token is:\n{refresh_token}\n")
        print("Add this to your .env file as AVS_REFRESH_TOKEN")
    except Exception as e:
        print(f"Error: {e}")