import os.path
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1erIdl-wkWvE8P2_YWas6ZUpsyimeCaJdvhLsoHrctv0"
SAMPLE_RANGE_NAME = "Sheet1!A1"

def main():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=3000)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    tweet_data = extractData()
    print(tweet_data)
    valueData = [['ac'],['gg']]
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
      sheet.values()
        .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,valueInputOption="USER_ENTERED",body={"values":tweet_data}).execute())

  except HttpError as err:
    print(err)

def extractData():
  api_url = 'https://twitter154.p.rapidapi.com/user/tweets'

  # Define query parameters
  params = {
    'username': 'omarmhaimdat'
    # Add more parameters as needed
  }

  # Define custom headers
  headers = {
    'X-RapidAPI-Key': 'ca2f27389emsh90d9a9bf33dacc5p1f3fb3jsn28df763a85b1',  # Include any necessary authorization headers
    'X-RapidAPI-Host': 'twitter154.p.rapidapi.com',  # Include a user agent header
    # Add more headers as needed
  }

  # Make the GET request with query parameters and headers
  response = requests.get(api_url, params=params, headers=headers)
  tweet_data = []

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
      # Extract information from the response
      data = response.json()
      
      results = data.get('results', []) 

      for i in range(15):
          if results:
              if 'retweet_status' in results[i]:
                  print(i)
                  text_inside_retweet_status = results[i].get('text', None)
                  print(text_inside_retweet_status+"\n")
                  tweet_data.append([i + 1, text_inside_retweet_status])
                  print("Data has been added to the Google Sheet.")
              else:
                  print("The tweet is not a retweet.")
          else:
              print("No results found in the response.")
     
          
  else:
      print(f"Error: {response.status_code}, {response.text}")
  return tweet_data


if __name__ == "__main__":
  main()