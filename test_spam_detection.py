import requests
from bs4 import BeautifulSoup

# URL of your FastAPI form endpoint
url = "http://127.0.0.1:8000/"

# Data to be submitted with the form
data = {
    "first_name": "Test",
    "last_name": "User",
    "email": "vanessa@example.com",
    "country": "Europe",  
    "message": "Test message",
    "gender": "P",
    "subject": "Order",
    "website": "spam"  # Honeypot field filled out
}

# Send the POST request
response = requests.post(url, data=data)

# Check if the response is successful
if response.status_code == 200:
    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the "Spam detected" message
    error_message = soup.find('h1').text if soup.find('h1') else "No error message found"
    print(error_message)
else:
    print("Test failed, status code:", response.status_code)
