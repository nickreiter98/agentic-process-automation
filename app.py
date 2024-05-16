import pickle
import logging

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)

from src.execution.executer import Executor
from src.modelling.model_generation import generate_model

if __name__ == '__main__':
   logging.basicConfig(filename='build/log.log',
                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     datefmt='%H:%M:%S',
                     level=logging.INFO)
   logger = logging.getLogger("httpx")
   logger.setLevel(logging.CRITICAL)
   logger = logging.getLogger(__name__)


   prompts = {
   'boss' : 'you are writing an email and sending the email to your boss. if the email is not sent, you will be fired. if the email is send you are gonna be promoted?',
   'weather_love_poem' : 'Get the weather data about berlin. If it is warmer than 10celsius write a love poem about the current weather, if colder write a negativ review abaout berlin. in both cases store the text in a file',
   'bank_statement' : 'Get the bank statement of the user with the id 2554727. If he has more than 1000€ in his account, send him a message that he is rich. If he has less than 1000€, send him a message that he is poor.',
   'weather_statement' : 'Get the weather data about berlin. Then write a love poem about the current weather and a negativ review about Berlin. Afterwards store the text of both text in a file. After storing both text can also are sent to nick.reiter@hotmail.de',
   'online_shop' : 'Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. After selecting the items, the user chooses between multiple options for a free reward. Since the reward value depends on the purchase value, this step is done after selecting the items, but it is independent of the payment activities',
   'expense_report' : 'read the uplaoded receipt, compile the the receipt into an expense report. The report is send to the nick.reiter@hotmail.de via email. if the report is approved, check if expenses are in compliance with the company policy. if the expenses are in compliance with the company policy. If yes, reimburse the money in the next payment cycle and notify me in the end.',
   'ticketing' : 'receive the following email, analyze the content of the email and assign the email to a category. Based on the category route the ticket to its responsible team. Send an email to the sendet with a short confirmation',
   'wikipedia' : 'Read the wikipedia page xxxx, store the text file and then transcribe it into ',
   'type_of_text' : '''When I send a worksheet of business lines through Web, deal with them according to which type of each business line belong to.
   1. To-Customer: Send a message to Slack to report the profits of business lines.
   2. To-Business: Write a report which should analyze the data to give some suggestions and then send it to the Gmail of the corresponding managers.''',
   'social_media_post' : 'The upcoming workflow begins with a trigger: new content is published on a blog via the RSS Feed or WordPress. The first action involves generating a summary using OpenAI to create a concise overview of the new blog post. Next, posts are scheduled across social media platforms. For LinkedIn, a post is scheduled containing the summary and a link to the blog; for Twitter, a tweet is scheduled with the summary and a blog link; and for Facebook, a post is scheduled with the summary and the blog link. The third action is to notify the marketing team via Slack by sending a message in the designated Slack channel, providing details of the new blog post and the social media schedule. Finally, post data is logged into Google Sheets for performance tracking. A new row is added containing the blog post title, publication date, scheduled social media platforms, the summary, and links to the scheduled posts.',
   'customer_support_request' : 'When a new customer support request is received in the helpdesk (Zendesk/Freshdesk), the first action is to identify the topic and urgency using sentiment analysis. Then, an initial response is generated using OpenAI or pre-written templates. The request is assigned to the appropriate team member, who is notified via email or Slack. Finally, the ticket data is logged into Google Sheets for reporting purposes.',
   'loan_approval' : 'The loan approval process starts by receiving a customer request for a loan amount. The risk assessment Web service is invoked to assess the request. If the loan is small and the customer is low risk, the loan is approved. If the customer is high risk, the loan is denied. If the customer needs further review or the loan amount is for $10,000 or more, the request is sent to the approver Web service. The customer receives feedback from the assessor or approver.',
   'wikipedia' : 'read the wikipedia page of Waldkirch, summarize it and then upload it to Medium and also send it toemail address nick.reiter@hotmail.de',
   'bank_check': 'get the bank statement of user 123456. Then check simultaneously whether the user already had financial issues and also get his last ten transactions. If the user already had fincancial issues, write a warning message and send him an email test-user@web.de, if not send him an email that the user is short of money. Also summarize the last 10 transactions and store it on my pc.',
   'creative' : 'write a creative text about a locust swimming in the ocean. Afterwards send the text to the email nick.reiter, also transform the text into a voice message and send it as a appendix to nick.reiter@hotmail.de. last but not least, trasnform the text into a picture and send it as well via email '
   # prompt = 'analyze an email and check via virustotal whether the text contains virus
   # prompt = stock analysis and prediction
   }

   ### TODO --> Split in batches Node

   process = generate_model(prompts['creative'])
   #process.save_bpmn()
   ### TODO --> Split in batches Node
   
   #logging.info(prompts['weather_love_poem'])
   #process = generate_model(prompts['weather_love_poem'])
   #logging.info(process.__str__())

   print(process.__str__())


   with open('_dev_bpmn/process_object_creative.pkl', 'wb') as outp:
             pickle.dump(process, outp)

   #with open('_dev_bpmn/process_object_wikipedia.pkl', 'rb') as inp:
   #   process = pickle.load(inp)

   #print(process.__str__())



   # executer = Executor(prompts['wikipedia'], process)
   # new_workflow = executer.run()

   # TODO Converging simultaneous gateways
   # TODO Convergin exclusive gateways