import pickle
import logging

from execution.executer import Executor
from modelling.model_generation import generate_model

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    prompts = {
    'boss' : 'you are writing an email and sending the email to your boss. if the email is not sent, you will be fired. if the email is send you are gonna be promoted?',
    'weather_love_poem' : 'Get the weather data about berlin. If it is warmer than 10celsius write a love poem about the current weather, if colder write a negativ review abaout berlin. in both cases store the text in a file',
    'bank_statement' : 'Get the bank statement of the user with the id 2554727. If he has more than 1000€ in his account, send him a message that he is rich. If he has less than 1000€, send him a message that he is poor.',
    'weather_statement' : 'Get the weather data about berlin. Then write a love poem about the current weather and a negativ review about Berlin. Afterwards store the text of both text parallely in a file',
    'online_shop' : 'Consider a process for purchasing items from an online shop. The user starts an order by logging in to their account. Then, the user simultaneously selects the items to purchase and sets a payment method. Afterward, the user either pays or completes an installment agreement. After selecting the items, the user chooses between multiple options for a free reward. Since the reward value depends on the purchase value, this step is done after selecting the items, but it is independent of the payment activities',
    'expense_report' : 'read the uplaoded receipt, compile the the receipt into an expense report. The report is send to the nick.reiter@hotmail.de via email. if the report is approved, check if expenses are in compliance with the company policy. if the expenses are in compliance with the company policy. If yes, reimburse the money in the next payment cycle and notify me in the end.',
    'ticketing' : 'receive the following email, analyze the content of the email and assign the email to a category. Based on the category route the ticket to its responsible team. Send an email to the sendet with a short confirmation',
    'wikipedia' : 'Read the wikipedia page xxxx, store the text file and then transcribe it into my ass '
    # prompt = 'analyze an email and check via virustotal whether the text contains virus
    # prompt = stock analysis and prediction
    }

    ### TODO --> Split in batches Node

    process = generate_model(prompts['weather_love_poem'])

    logging.info(process.__str__())

    #with open('_dev_bpmn/process_object_weather_love_poem.pkl', 'wb') as outp:
    #           pickle.dump(process, outp)

    #with open('_dev_bpmn/process_object_weather_love_poem.pkl', 'rb') as inp:
    #    process = pickle.load(inp)

    executer = Executor(prompts['weather_love_poem'], process)
    new_workflow = executer.run()