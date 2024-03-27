import requests
import json
import os
import base64

from dotenv import load_dotenv
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv('.env')

def d_get_current_weather(city: str):
    """provides current weather data for a given city

    :param city: name of the city
    :return: current weather parameters
    """
    url = 'http://api.weatherapi.com/v1/current.json'
    req = requests.get(
        url=url,
        params={
            'key': os.getenv('WEATHER_API_KEY'),
            'q': city
        }
    )
    return req.json()
    

def d_get_coordinates_by_city(city: str):
    """provides coordinates of a given city

    :param city: name of the city
    :return: coordinates of the city
    """
    
    url = 'https://nominatim.openstreetmap.org/search'
    req = requests.get(
        url=url,
        params={
            'q': city,
            'format': 'json'
        }
    )
    return req.json()

def d_send_email_to(recipient: str, content: str, subject: str):
    """sends an email to a given recipient

    :param recipient: email address of the recipient
    :param content: content of the email to be sent
    :param subject: subject of the email to be sent
    """
    CLIENT_FILE = 'account_01.json'
    SCOPES = ['https://mail.google.com/']

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    message = EmailMessage()
    message.set_content(content)
    message['To'] = recipient
    message['From'] = 'nick.reiter6.11.98@gmail.com'
    message['Subject'] = subject

    raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {'raw': raw_string}

    send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )


 