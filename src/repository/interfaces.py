import requests
import json
import os
import base64
import logging

from dotenv import load_dotenv
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from openai import OpenAI

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
    CLIENT_FILE = 'config/account_01.json'
    SCOPES = ['https://mail.google.com/']

    creds = None

    if os.path.exists('config/token.json'):
        creds = Credentials.from_authorized_user_file('config/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('config/token.json', 'w') as token:
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

def d_write_text(text_content:str, context_info:str) -> str:
    """formulates the text content based on the context information.
    Is needed for created a nice sounding text output

    :param text_content: text plain content to be formulated
    :param context_info: context information shaping the text - informal, formal, audience, recipient, etc.
    :return: nicely formulated text
    """
    client = OpenAI()

    SYS_MESSAGE = """
    You are a text writer and wants to be precise.
    Write a nice sounding text and use for it content information and context.
    The context is shaping the formality, the audience, the tone, etc.
    """

    prompt = f"""
    Write a nice sounding text.
    Include the following context information:
    {text_content}
    and formulate the text concerning following information:
    {context_info}
    """

    res = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': SYS_MESSAGE},
            {'role': 'user', 'content': prompt}
        ]
    )

    output = res.choices[0].message.content

    return output

def d_store_text_to_disc(content:str, file_name:str):
    """stores any textual representation in a file

    :param content: any representation containing string to be stored
    :param file_name: name of the .txt file
    """
    with open(f'output/{file_name}', 'w') as f:
        f.write(content)

def d_get_bank_account_statement(user_id:int) -> dict:
    """provides the bank account statement of a user

    :param use_id: id of the user
    :return: bank account statement of the user
    """
    import random

    account_type = random.choice(['business', 'private'])
    balance = round(random.uniform(-10000, 100000), 2)
    return {
        'user_id': user_id,
        'properties':{
            'name': 'Max Muster',
            'iban': 'DE123456789054672',
            'bic': 'GENODEF1M03',},
        'balance': balance,
        'account_type': account_type
    }



 