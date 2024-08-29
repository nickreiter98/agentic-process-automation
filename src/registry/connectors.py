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
import random

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
def get_current_weather(city: str):
    """provides current weather data for a given city

    :param city: name of the city
    :return: current weather parameters
    """
    api_key = os.getenv('WEATHER_API_KEY')
    url = 'http://api.weatherapi.com/v1/current.json'
    req = requests.get(
        url=url,
        params={
            'key': api_key,
            'q': city
        }
    )
    return req.json()
    

def get_coordinates_by_city(city: str):
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


def write_text(text_content:str, context_info:str) -> str:
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

    return {'written_text': output}

def store_text_to_disc(content:str, file_name:str):
    """stores any textual representation in a file

    :param content: any representation containing string to be stored
    :param file_name: name of the .txt file
    """
    with open(f'output/{file_name}', 'w') as f:
        f.write(content)

def get_bank_account_statement(user_id:int) -> dict:
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
            'bic': 'GENODEF1M03',
            'email': 'nick.reiter@hotmail.de'},
        'balance': balance,
        'account_type': account_type
    }

def get_wikipedia_page(page:str) -> str:
    """provides the content of a wikipedia page

    :param page: name of the wikipedia page
    :return: content of the wikipedia page
    """
    def _request(page):
        response = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params={
                'action': 'query',
                'format': 'json',
                'titles': page,
                'prop': 'revisions',
                'rvprop': 'content',
                'redirects': 1
            }).json()
        return response
    
    try:
        response = _request(page)
        try:
            response['query']['redirects'][0]['to']
            page = response['query']['redirects'][0]['to']
            response = _request(page)
        except Exception:
            pass
        page = next(iter(response['query']['pages'].values()))
        wikicode = page['revisions'][0]['*']
        parsed_wikicode = mwparserfromhell.parse(wikicode)
        return {'wikipedia_text':parsed_wikicode.strip_code()}
    except Exception as e:
        raise Exception(f"Error while getting the wikipedia page with {e}")

def apply_natural_language_task(content: str, task: str) -> str:
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

    return {'transformd_etextual_content':output}

def upload_to_medium(content:str, title:str) -> dict:
    """uploads a blog post to medium

    :param content: content of the blog post
    :param title: title of the blog post
    """
    exemplaric_response = {
        "status": "Successfully uploaded blog post",
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
def get_basic_financials(name:str, type:TYPE='all_metric') -> dict:
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

def create_image_from_text(description:str) -> str:
    """creates any desired image from a text description

    :param description: the description/prompt of the image to create
    :return: path to the temporary file
    """
    # dalle cannot handle more than 1000 tokens
    description = description.split(" ")
    if len(description) > 100:
        description = " ".join(description[:100])
    else:
        description = " ".join(description)
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

def store_image_to_disk(path_name:str, filename:str="output") -> None:
    """stores the image to disk

    :param path_name: path to the temporary file
    :param filename: filename of the image to store, defaults to "output"
    """
    shutil.copy(path_name, f'output/{filename}.jpg')

def transform_text_to_speech(text: str, lang: str='en') -> str:
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

def store_speech_to_disk(path_name:str, filename:str='output') -> None:
    """stores the speech to disk

    :param path_name: path to the temporary file
    :param filename: name of the file to store the speech, defaults to 'output'
    """
    shutil.copy(path_name, f'output/{filename}.mp3')


def get_dhl_tracking_history(id:str) -> dict:
    """get the tracking history of a shipment from DHL

    :param id: the tracking number of the shipment
    :return: the tracking history of the shipment
    """

    tracking_history = {
        "shipmentTrackingResponse": {
            "trackingNumber": id,
            "status": "success",
            "shipmentDetails": {
            "shipmentID": "0987654321",
            "service": "Express",
            "origin": {
                "country": "Germany",
                "city": "Berlin",
                "postalCode": "10115"
            },
            "destination": {
                "country": "USA",
                "city": "New York",
                "postalCode": "10001"
            },
            "pickupDate": "2023-06-15T10:00:00Z",
            "deliveryDate": "2023-06-18T15:00:00Z",
            "currentStatus": "Delivered",
            "weight": {
                "value": 2.5,
                "unit": "kg"
            },
            "dimensions": {
                "length": 30,
                "width": 20,
                "height": 10,
                "unit": "cm"
            }
            },
            "events": [
            {
                "timestamp": "2023-06-15T10:00:00Z",
                "location": "Berlin, Germany",
                "status": "Shipment picked up"
            },
            {
                "timestamp": "2023-06-16T12:00:00Z",
                "location": "Leipzig, Germany",
                "status": "Shipment in transit"
            },
            {
                "timestamp": "2023-06-17T08:00:00Z",
                "location": "London, UK",
                "status": "Customs clearance completed"
            },
            {
                "timestamp": "2023-06-18T15:00:00Z",
                "location": "New York, USA",
                "status": "Delivered"
            }
            ]
        }
    }
    return tracking_history

def get_banking_account_summary(user_id:int) -> dict:
    """Get the banking account summary of a user inlcuding the balance and the last 10 transactions

    :param user_id: the id of the user
    :return: the banking account summary including the balance and the last 10 transactions
    """
    financial_issue = random.choice([True, False])
    summary ={
        "userId": "123456",
        "userEmail": "test-user@web.de",
        "bankStatement": {
            "balance": 150.75,
            "transactions": [
            {
                "date": "2024-06-01",
                "description": "Grocery Store",
                "amount": -50.25
            },
            {
                "date": "2024-06-03",
                "description": "Salary",
                "amount": 2000.00
            },
            {
                "date": "2024-06-05",
                "description": "Electricity Bill",
                "amount": -100.75
            },
            {
                "date": "2024-06-07",
                "description": "Gas Station",
                "amount": -40.00
            },
            {
                "date": "2024-06-10",
                "description": "Gym Membership",
                "amount": -30.00
            },
            {
                "date": "2024-06-12",
                "description": "Dinner",
                "amount": -60.00
            },
            {
                "date": "2024-06-14",
                "description": "Rent",
                "amount": -800.00
            },
            {
                "date": "2024-06-16",
                "description": "Internet Bill",
                "amount": -50.00
            },
            {
                "date": "2024-06-18",
                "description": "Car Payment",
                "amount": -250.00
            },
            {
                "date": "2024-06-19",
                "description": "Medical Bill",
                "amount": -100.00
            }
            ]
        },
        "financialIssues": financial_issue
    }

    return summary


def get_credit_score(user_id:int) -> dict:
    """Get the credit score of a user

    :param user_id: the id of the user
    :return: information about the credit score of the user
    """
    score = random.randint(300, 850)
    credit_score = {
        "status": "success",
        "data": {
            "customer_id": user_id,
            "credit_score": {
            "score": score,
            "score_range": {
                "min": 300,
                "max": 850
            },
            "risk_level": "low",
            "last_updated": "2024-07-03T10:15:30Z"
            },
            "customer_details": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
            }
        },
        "metadata": {
            "request_id": "abc123xyz",
            "timestamp": "2024-07-03T10:20:00Z"
        }
    }
    return credit_score



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

def send_email_to(recipient: str, content: str, subject: str, file:str=None):
    """sends an email to a given recipient. Optionally, a file (voice message, PDF
    document, image, etc.) can be attached to the email.

    :param recipient: email address of the recipient
    :param content: content of the email to be sent
    :param subject: subject of the email to be sent
    :param path_name: path to the temporary file to be attached (image, pdf, etc.)
    """
    credentials = _get_google_oauth_credentials()

    service = build('gmail', 'v1', credentials=credentials)

    message = MIMEMultipart()
    message['To'] = recipient
    message['From'] = os.getenv('EMAIL_SENDER')
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
    
    if 'id' in send_message:
        return {"status": "Successfully sent email"}
    else:
        return {"status": "Failed to send email"}
    
def get_google_document(document_id:str) -> dict[str, str]:
    """get the text content of a google document

    :param document_id: document id of the google document
    :return: text content of the document
    """
    credentials = _get_google_oauth_credentials()

    service = build('docs', 'v1', credentials=credentials)
    document = service.documents().get(documentId=document_id).execute()

    content = document.get('body').get('content')

    text = ''
    for element in content:
        if 'paragraph' in element:
            for paragraph_element in element['paragraph']['elements']:
                if 'textRun' in paragraph_element:
                    text += paragraph_element['textRun']['content']

    return {'google_document_text':text}

def create_google_document(title:str) -> dict[str, str]:
    """create a new google document

    :param title: the title of the new document
    :return: document id of the new document
    """
    credentials = _get_google_oauth_credentials()

    service = build('docs', 'v1', credentials=credentials)
    document = {
        'title': title
    }
    document = service.documents().create(body=document).execute()
    document_id = document.get('documentId')
    return {'google_document_id':document_id}


def update_google_document(text:str, document_id:str):
    """update the text content of a google document.
    The text will be appended to the end of the document.

    :param text: text to be appended to the document
    :param document_id: document id of the google document
    """
    credentials = _get_google_oauth_credentials()
    service = build('docs', 'v1', credentials=credentials)

    document = service.documents().get(documentId=document_id).execute()
    content = document.get('body').get('content')
    last_element = content[-1]
    end_index = last_element.get('endIndex')

    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index-1,
                },
                'text': text
            }
        }
    ]
    body = {'requests': requests}

    document = service.documents().batchUpdate(documentId=document_id, body=body).execute()

def get_latest_email() -> dict[str, str]:
    """get the latest email from Google Mail

    :return: a dictionary containing the email subject,
    sender and text of the lates email
    """
    creds = _get_google_oauth_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    results = service.users().messages().list(userId='me', maxResults=1, q='is:inbox').execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
        return None

    latest_message_id = messages[0]['id']
    message = service.users().messages().get(userId='me', id=latest_message_id).execute()

    # Decode the email message
    payload = message['payload']
    headers = payload['headers']
    parts = payload.get('parts', [])
    data = ''
    
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                break
    else:
        data = payload['body']['data']
        
    email_text = base64.urlsafe_b64decode(data).decode('utf-8')
    
    email_subject = next(header['value'] for header in headers if header['name'] == 'Subject')
    email_from = next(header['value'] for header in headers if header['name'] == 'From')
    
    return {
        'subject': email_subject,
        'from': email_from,
        'text': email_text
    }
    
def get_values_from_google_sheet(spreadsheet_id:str, range_notation:str='Sheet1') -> dict:
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

def append_values_to_google_sheet(spreadsheet_id:str, values:list[list[str]], range_name:str='Sheet1'):
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

def create_new_google_sheet(title:str) -> dict[str, str]:
    """Create a new google sheet spreadsheet

    :param title: title of the new spreadsheet
    :return: dictionary containing the spreadsheet ID
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
    return {"spreadsheet_id": f"{spreadsheet.get('spreadsheetId')}"}

from typing import List
def append_values_to_google_sheet(spreadsheet_id:str, values:List[List[str]]):
    """Append values to a google sheet
    
    :param spreadsheet_id: ID of the google sheet
    :param values: List of values to be appended. Is represented as 2D list, where each inner list represents a row
    """
    credentials = _get_google_oauth_credentials()
    
    service = build("sheets", "v4", credentials=credentials)

    body = {
        'values': values
    }

    range_name:str='Tabellenblatt1'

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

def get_values_from_google_sheet(spreadsheet_id:str, range_notation:str='Tabellenblatt1') -> dict:
    """
    :param spreadsheet_id: id of the google sheet
    :param range_noation: range of values to be retrieved in A1 notation
    :return: dictionary containing the values of the google sheet
    """
    credentials = _get_google_oauth_credentials()

    service = build("sheets", "v4", credentials=credentials)

    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_notation)
    values = request.execute()

    return values

def create_event_in_calender(start_datetime:str, end_datetime:str, summary:str):
    """creates an event in a google calendar

    :param start_datetime: the start time of the event in RFC3339 format
    :param end_datetime: end time of the event in RFC3339 format
    :param summary: _description of the event
    :param calendar_id: the id of the calendar to create the event in
    """

    event = {
        "end": {
            "dateTime": end_datetime
        },
        "start": {
            "dateTime": start_datetime
        },
        "summary": summary,
    }

    calendar_id:str = "nick.reiter6.11.98@gmail.com"
    credentials = _get_google_oauth_credentials()
    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().insert(calendarId=calendar_id, body=event).execute()

############## END GOOGLE APIS ############




 