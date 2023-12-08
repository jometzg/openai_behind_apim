# A sample Python app that calls the OpenAI API via Azure API Management (APIM)
# and uses the MSAL Python library to authenticate with Azure AD

import msal
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# Define your Azure AD app credentials
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
AUTHORITY = os.environ.get("AZURE_AUTHORITY")
SCOPE = os.environ.get("AZURE_SCOPE")
APIM_SUBSCRIPTION_KEY = os.environ.get("APIM_SUBSCRIPTION_KEY")
OPEN_AI_COMPLETION_ENDPOINT = os.environ.get("OPEN_AI_COMPLETION_ENDPOINT")

# make sure we don't get this multiple times
access_token = None

def get_access_token():
    """
    Retrieves the access token from Azure AD using interactive authentication.

    Returns:
        str: The access token.
    """
    global access_token
    if access_token is None:
        # Create a PublicClientApplication instance
        app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
        scope = [SCOPE]
        # Acquire a token using interactive authentication
        result = app.acquire_token_interactive(scope)

        # Check if the authentication was successful
        if "access_token" in result:
            # Use the access token to make authenticated API calls
            access_token = result["access_token"]
        else:
            print(result.get("error_description", "Authentication failed."))
    return access_token

def query_openai_api(query):
    """
    Queries the OpenAI API via APIM and returns the response.

    Args:
        query (str): The user's query.

    Returns:
        str: The response from the OpenAI API.
    """
    # now call the OpenAI API via APIM
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": APIM_SUBSCRIPTION_KEY,
        "Ocp-Apim-Trace": "true"
    }
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "you are a helpful AI assistant that helps car purchasing tasks"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }
    response = requests.post(OPEN_AI_COMPLETION_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 200:
        res = response.json()
        return res["choices"][0]["message"]["content"]
    else:
        print("Error calling APIM: " + str(response.status_code))
        return None
    
def main():
    """
    The main function of the application.
    """
    get_access_token()
    if access_token is not None:
        print("Successfully authenticated")
        print("Access token: " + access_token)
        print("Calling OpenAI API")
        query = "I am looking for a car that is reliable and affordable"
        response = query_openai_api(query)
        print("Response: " + response)

if __name__ == "__main__":
    main()
