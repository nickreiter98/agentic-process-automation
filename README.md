# Agentic Process Automization 🤖
## 📚 Content
This repository contains the coding part of the Master's Thesis "Agentic Process Automization: A LLM-backed approach to automatically execute Textual Process Workflows"

The software primarily aims to automize the execution of textual process workflows. The workflows can take the form of workflows executed by drag-and-drop solutions like [n8n](https://n8n.io/). This implies that activities must be modelled as interfaces. Whether they are real APIs or locally run scripts does not matter. Below an exemplaric and executable workflow is given.

> Get the current weather in Berlin. If it is warmer than 10 Celsius, write a positive review about Berlin. If it is colder, write a negativ review about Berlin. In both cases, store the text locally in a file.

To successfully execute the textual workflow only with the help of LLM - *in this case the OpenAI API with the model gpt-4o* - two agents are created:\
**Modeller:** This agent transform the textual workflow into a BPMN-like representation. For this, we bring the the agent to autonomously code a BPMN-like instance. The BPMN-like class is derived from Frauenhofer's [PM4PY](https://pm4py.fit.fraunhofer.de/) Python library.\
**executor:** This agent is subdivided into a module which selects for each activity the proper function from the function repository and a module which assigns the selected function's paramete with the appropriate arguments. This agent strongly resembles the function calling mechanism of LLM frameworks.

To feed the upper agents with information, the programm contains a repository:\
**Function Repository:** The repository contains the connection to all interfaces -*APIs or locally implemented functions*. These connections are represented as well annotated python functions. Also the repository class offers functions which transform the interfaces into string representations to make the informations processable for the LLM.

## ⚙️ Initialization
### Initialization
**Environmnet & required Libraries:** To prepare for execution you have to install an enviroment and all required libraries. To to this run in your shell `./init.sh`

**API Keys:** To execute the software, API keys are required. The required API keys you can add to the `.env` file. Please keep all keys. Required is the OpenAI Key, you cann get from the company's webside

**Google APIs:** So far, to test the software, Google APIs are excessively used. To activate this please follow this [tutorial](https://developers.google.com/identity/protocols/oauth2) and activate and get the OAuth 2.0-Client-ID for the following APIs: *Google Mail, Google Sheets, Google Docs and Google Calendar*. Please store the client key `config/account_01.json`

### Example
**Textual Workflow:** Get the current weather data about Berlin. If it is warmer than 10 Celsius write a love poem about the current weather. If colder, write a negative review about Berlin. In both cases store the text in a file wit the name "yippiii_berlin"

**Streamlit:** 
1. Modelling textual workflow

![](docs/screenshot_streamlit_01.png)

2. Executing textual workflow

![](docs/screenshot_streamlit_02.png)



## 🚀 Execution
First at all activate your environment: `source .venv/bin/activate`

There are three different ways, you can execute the software:

**Streamlit:** To execute the software with a nice GUI, you have to run the programm with `streamlit run app_st.py` in your shell

**Terminal** Enter into your terminal `python3 app.py`. Then you can interact with the console and type in your desired workflow to execute

**Test:** To run tests on your local machine, please move to the directory test `cd test` and then start the test script with `python3 app_test.py`. You can change the textual workflows to test in the `workflow_description.csv` file. It stores the output of a run in pdf.





