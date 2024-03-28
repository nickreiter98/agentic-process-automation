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
    logging.info(f'START: d_get_current_weather | args: {city}')
    url = 'http://api.weatherapi.com/v1/current.json'
    req = requests.get(
        url=url,
        params={
            'key': os.getenv('WEATHER_API_KEY'),
            'q': city
        }
    )
    logging.info(f'END: d_get_current_weather | response: {req.json()}')
    return req.json()
    

def d_get_coordinates_by_city(city: str):
    """provides coordinates of a given city

    :param city: name of the city
    :return: coordinates of the city
    """
    logging.info(f'START: d_get_coordinates_by_city | args: {city}')
    url = 'https://nominatim.openstreetmap.org/search'
    req = requests.get(
        url=url,
        params={
            'q': city,
            'format': 'json'
        }
    )
    logging.info(f'END: d_get_coordinates_by_city | response: {req.json()}')
    return req.json()

def d_send_email_to(recipient: str, content: str, subject: str):
    """sends an email to a given recipient

    :param recipient: email address of the recipient
    :param content: content of the email to be sent
    :param subject: subject of the email to be sent
    """
    logging.info(f'START: d_send_email_to | args: {recipient}, {content}, {subject}')
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
    logging.info(f'END: d_send_email_to | response: {send_message}')

def d_write_text(text_content:str, context_info:str) -> str:
    """formulates the text content based on the context information.
    Is needed for created a nice sounding text output

    :param text_content: text content to be formulated
    :param context_info: context information shaping the text - informal, formal, audience, etc.
    :return: nicely formulated text
    """
    logging.info(f'START: d_write_text | args: {text_content}, {context_info}')
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
        model='gpt-4-0613',
        messages=[
            {'role': 'system', 'content': SYS_MESSAGE},
            {'role': 'user', 'content': prompt}
        ]
    )

    output = res.choices[0].message.content

    logging.info(f'END: d_write_text | response: {output}')
    return output


 