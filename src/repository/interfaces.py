import requests
import os
import base64
import requests
import mwparserfromhell
import re
import finnhub
import io
import pickle
import tempfile
import mimetypes
import shutil

from dotenv import load_dotenv
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from openai import OpenAI
from typing import Literal
from PIL import Image
from gtts import gTTS

load_dotenv('.env')

############ START GENERAL FUNCTIONS ############
def _store_tempfile(data: object) -> dict:
    """stores a temporary file with the data

    :param data: data to store in the temporary file
    :return: path to the temporary file
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        pickle.dump(data, temp)
        return {'path_name': temp.name}
    

def _load_tempfile(path: str) -> object:
    """loads a temporary file with the data

    :param path: path to the temporary file
    :return: data stored in the temporary file
    """
    with open(path, 'rb') as temp:
        data = pickle.load(temp)
        return data
############ END GENERAL FUNCTIONS ############

############ START API FUNCTIONS ############
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


def d_write_text(text_content:str, context_info:str) -> str:
    """formulates any type of text content for any type of text like email, letter, advertisement etc. .
    Provides a nicely formulated text based on the given context information.

    :param text_content: plain text content to be formulated
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

def d_get_wikipedia_page(page:str) -> str:
    """provides the content of a wikipedia page

    :param page: name of the wikipedia page
    :return: content of the wikipedia page
    """
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': page,
            'prop': 'revisions',
            'rvprop': 'content'
        }).json()
    page = next(iter(response['query']['pages'].values()))
    wikicode = page['revisions'][0]['*']
    parsed_wikicode = mwparserfromhell.parse(wikicode)
    return parsed_wikicode.strip_code()

def d_apply_natural_language_task(content: str, task: str) -> str:
    """
    Transforms textual content based on the specified task.
    This function takes textual content and a specified transformation task as input, and performds the
    transformation. Tasks can range from summarizing to rewriting, translating, or creating new content based on prompts.

    :param content: The input textual content to be transformed. This can include paragraphs, documents, or specific text prompts.
    :param task: A clear instruction specifying the transformation task. Example tasks include:
            - "Summarize the following content."
            - "Rewrite the following content in simpler language."
            - "Translate the following content to French."
            - "Provide a more detailed explanation of the following content."
            - "Create a creative story based on the following prompt."

    :return: The transformed textual content based on the specified task.
    """
    prompt = f"{task}\n\n{content}"

    res = OpenAI().chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant that can transform text based on specific tasks.'},
            {'role': 'user', 'content': prompt}
        ]
    )

    output = res.choices[0].message.content

    return output

def d_upload_to_medium(content:str, title:str) -> dict:
    """uploads a blog post to medium

    :param content: content of the blog post
    :param title: title of the blog post
    """
    exemplaric_response = {
        "data": {
            "id": "e6e862f2e6e1",
            "title": "Hello, Medium!",
            "authorId": "f8d5d2b0e6d0",
            "tags": ["Medium", "API", "Python"],
            "url": "https://medium.com/@your_username/hello-medium-e6e862f2e6e1",
            "canonicalUrl": "",
            "publishStatus": "draft",
            "publishedAt": 'null',
            "license": "all-rights-reserved",
            "licenseUrl": "https://medium.com/policy/9db0094a1e0f",
            "createdAt": 1686503123456,
            "updatedAt": 1686503123456
        }
        }

    return exemplaric_response

TYPE = Literal['52week', 'revenue', 'all_metrics']
def d_get_basic_financials(name:str, type:TYPE='all_metric') -> dict:
    """Get company basic financials such as margin, P/E ratio, 52-week high/low etc.

    :param name: the name of the company to search for
    :param type: the type of financials to return. Default is 'all_metrics'
    :return: a dictionary of the requested financials
    """
    key = os.getenv('FINNHUB_API_KEY')
    client = finnhub.Client(api_key=key)

    lookup = client.symbol_lookup(name)
    symbol = lookup['result'][0]['symbol']
    response = client.company_basic_financials(symbol, 'all')

    if type == '52week':
        keys = ['52WeekHigh','52WeekHighDate','52WeekLow','52WeekLowDate', '52WeekPriceReturnDaily']
        new_dict = {key: response['metric'][key] for key in keys}
        return new_dict
    elif type == 'revenue':
        new_dict = {key: response['metric'][key] for key in response['metric'] if re.search('revenue', key, re.IGNORECASE)}
        return new_dict
    elif type == 'all_metrics':
        return response['metric']
    else:
        return response

def d_create_image_from_text(description:str) -> str:
    """creates any desired image from a text description

    :param description: the description/prompt of the image to create
    :return: path to the temporary file
    """
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.images.generate(
        model="dall-e-2",
        prompt=description,
        n=1,
        size="1024x1024"
    )

    image_url = response.data[0].url
    image_data = requests.get(image_url)
    image = Image.open(io.BytesIO(image_data.content))

    with tempfile.NamedTemporaryFile(delete=False, prefix='picture_', suffix='.jpg') as temp:
        image.save(temp)
        path_name = temp.name
        return {'path_name': path_name}

def d_store_image_to_disk(path_name:str, filename:str="output") -> None:
    """stores the image to disk

    :param path_name: path to the temporary file
    :param filename: filename of the image to store, defaults to "output"
    """
    shutil.copy(path_name, f'output/{filename}.jpg')

def d_transform_text_to_speech(text: str, lang: str='en') -> str:
    """transforms amy desired text to speech

    :param text: text to convert to speech
    :param lang: language of the text, defaults to 'en'
    :return: path to the temporary file
    """
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, prefix='voice_', suffix='.mp3') as temp:
        tts.write_to_fp(temp)
        path_name = temp.name
        return {'path_name': path_name}

def d_store_speech_to_disk(path_name:str, filename:str='output') -> None:
    """stores the speech to disk

    :param path_name: path to the temporary file
    :param filename: name of the file to store the speech, defaults to 'output'
    """
    shutil.copy(path_name, f'output/{filename}.mp3')

############ END API FUNCTIONS ############

############ START GOOGLE APIS ############
def _get_google_oauth_credentials() -> Credentials:
    CLIENT_FILE = 'config/account_01.json'
    SCOPES = ['https://mail.google.com/',
          'https://www.googleapis.com/auth/documents',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/calendar']
    
    credentials = None
    
    if os.path.exists('config/token.json'):
        credentials = Credentials.from_authorized_user_file('config/token.json', SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('config/token.json', 'w') as token:
            token.write(credentials.to_json())

    return credentials

def d_send_email_to(recipient: str, content: str, subject: str, file:str=None):
    """sends an email to a given recipient. Optionally, a file can be attached to the email.

    :param recipient: email address of the recipient
    :param content: content of the email to be sent
    :param subject: subject of the email to be sent
    :param path_name: path to the temporary file to be attached (image, pdf, etc.)
    """
    credentials = _get_google_oauth_credentials()

    service = build('gmail', 'v1', credentials=credentials)

    message = MIMEMultipart()
    message['To'] = recipient
    message['From'] = 'nick.reiter6.11.98@gmail.com'
    message['Subject'] = subject

    msg = MIMEText(content)
    message.attach(msg)

    if file is not None:
        content_type, encoding = mimetypes.guess_type(file)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'r')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(msg)    
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
        message.attach(msg)

    raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {'raw': raw_string}

    send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
    
def d_get_values_from_google_sheet(spreadsheet_id:str, range_notation:str='Sheet1') -> dict:
    """

    :param spreadsheet_id: _description_
    :param range_noation: range of values to be retrieved in A1 notation
    :return: _description_
    """
    credentials = _get_google_oauth_credentials()

    service = build("sheets", "v4", credentials=credentials)

    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_notation)
    values = request.execute()

    return values

def d_append_values_to_google_sheet(spreadsheet_id:str, values:list[list[str]], range_name:str='Sheet1'):
    """
    
    :param spreadsheet_id: _description_
    :param range_name: range of values to be retrieved in A1 notation
    :param values: _description_
    :return: _description_
    """
    credentials = _get_google_oauth_credentials()
    
    service = build("sheets", "v4", credentials=credentials)

    body = {
        'values': values
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

# TODO: add content for spreadsheet
def d_create_new_google_sheet(title:str) -> str:
    """_summary_

    :param title: _description_
    :return: _description_
    """
    credentials = _get_google_oauth_credentials()
    
    service = build("sheets", "v4", credentials=credentials)

    spreadsheet = {
        'properties': {
            'title': title
        }
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                fields='spreadsheetId').execute()
    return f"'spreadsheet_id': '{spreadsheet.get('spreadsheetId')}'"
############## END GOOGLE APIS ############




 