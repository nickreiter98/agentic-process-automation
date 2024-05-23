import subprocess
import streamlit as st

from datetime import date

from src.execution.executer import Executor
from src.modelling.model_generation import generate_model
from src.utils.output_redirection import _print


def run_model_generator_app():
    subprocess.run(['streamlit', 'run', __file__])

def _modell(workflow:str):
    process = generate_model(workflow)
    return process

def _execute(process, workflow):
    executer = Executor(workflow, process)
    executer.run()
    return executer


def run_app():
    _print('+++++++++++++++++++++++')
    _print(f'NEW WORKFLOW WITH DATE: {date.today()}')
    _print('MODEL: gpt-4o')

    st.title('🤖 Agentic Process Automation')
    st.subheader("Automatic Textual Workflow Execution with Generative AI")

    with st.form(key='my_form'):
        col1, col2 = st.columns(2)

        with col1:
            api_key = st.text_input(
                'Enter your OpenAI API key here',
                type = 'password',
                help=(
                    ('You can get your API key from OpenAI'
                    ' by signing up at https://platform.openai.com/signup/')
                )
            )

        with col2:
            st.text("As default, Open AI's GPT-4o model is used")

        workflow = st.text_area(
            'Enter your workflow to be modelled and executed here',
        )        
        submit_button = st.form_submit_button(label='Run')

        _print(workflow)

    if submit_button:
        try:
            st.session_state['model_gen'] = _modell(workflow)
            st.session_state['feedback'] = []
        except Exception as e:
            st.error(body=str(e), icon="⚠️")


    if 'model_gen' in st.session_state and st.session_state['model_gen'] is not None:
        with st.form(key='modelling_form'):
            string_representation = st.session_state['model_gen'].__str__()
            pic_representation = st.session_state['model_gen'].get_bpmn()

            _print(string_representation)

            st.success("Workflow modelled successfully!", icon="🎉")
            with st.expander("View Image", expanded=True):
                    st.image(pic_representation.pipe(format='svg').decode('utf-8'))
            st.text('The workflow has been modelled as follows:\n\n'
                    f'{string_representation}\n\n')
            execution_button = st.form_submit_button('Execute Workflow')

            if execution_button:
                try:
                    st.session_state['model_exe'] = _execute(st.session_state['model_gen'], workflow)
                    st.session_state['feedback'] = []
                except Exception as e:
                    st.error(body=str(e), icon="⚠️")

            
            if 'model_exe' in st.session_state and st.session_state['model_exe'] is not None:
                log_representation = st.session_state['model_exe'].get_log()

                _print(log_representation)

                st.success("Workflow also executed successfully!", icon="🎉")
                st.text('The execution log is as follows:\n\n'
                        f'{log_representation}')


if __name__ == "__main__":
    st.set_page_config(
        page_title="Agentic Process Automation",
        page_icon="🤖"
    )
    run_app()