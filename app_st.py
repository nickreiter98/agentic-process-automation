import subprocess
import streamlit as st

from datetime import date

from src.execution.executor import WorkflowExecutor
from src.modelling.workflow_generation import generate_workflow


def run_model_generator_app():
    subprocess.run(["streamlit", "run", __file__])


def _modell(textual_workflow: str):
    workflow_processor, _ = generate_workflow(textual_workflow)
    return workflow_processor


def _execute(workflow_processor, textual_workflow: str):
    executor = WorkflowExecutor(textual_workflow, workflow_processor)
    executor.run()
    return executor


def run_app():
    st.title("🤖 Agentic Process Automation")
    st.subheader("Automatic Textual Workflow Execution with Generative AI")

    with st.form(key="my_form"):
        col1, col2 = st.columns(2)

        with col1:
            api_key = st.text_input(
                "Enter your OpenAI API key here",
                type="password",
                help=(
                    (
                        "You can get your API key from OpenAI "
                        "by signing up at https://platform.openai.com/signup/"
                    )
                ),
            )

        with col2:
            st.text("As default, Open AI's GPT-4o model is used")

        textual_workflow = st.text_area(
            "Enter your workflow to be modelled and executed here",
        )
        submit_button = st.form_submit_button(label="Run")

        print(textual_workflow)

    if submit_button:
        try:
            st.session_state["model_gen"] = _modell(textual_workflow)
            st.session_state["feedback"] = []
        except (Exception, RuntimeError) as e:
            st.error(body=str(e), icon="⚠️")

    if "model_gen" in st.session_state and st.session_state["model_gen"] is not None:
        with st.form(key="modelling_form"):
            workflow_str = st.session_state["model_gen"].__str__()
            workflow_image = st.session_state["model_gen"].get_bpmn()

            print(workflow_str)

            st.success("Workflow modelled successfully!", icon="🎉")
            with st.expander("View Image", expanded=True):
                st.image(workflow_image.pipe(format="svg").decode("utf-8"))
            st.text(
                "The workflow has been modelled as follows:\n\n"
                f"{workflow_str}\n\n"
            )
            execution_button = st.form_submit_button("Execute Workflow")

            if execution_button:
                try:
                    st.session_state["model_exe"] = _execute(
                        st.session_state["model_gen"], textual_workflow
                    )
                    st.session_state["feedback"] = []
                except Exception as e:
                    st.error(body=str(e), icon="⚠️")

            if (
                "model_exe" in st.session_state
                and st.session_state["model_exe"] is not None
            ):
                log_representation = st.session_state["model_exe"].get_log()

                print(log_representation)

                st.success("Workflow also executed successfully!", icon="🎉")
                st.text("The execution log is as follows:\n\n" f"{log_representation}")

if __name__ == "__main__":
    st.set_page_config(page_title="Agentic Process Automation", page_icon="🤖")
    run_app()