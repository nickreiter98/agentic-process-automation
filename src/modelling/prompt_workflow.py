import inspect

from src.modelling.prompt_workflow_few_shots import SHOTS, SHOTS_WITH_ERRORS

IMPORT_STATEMENT = "from src.modelling.generator import WorkflowProcessor"


def add_role():
    return (
        "Act as an expert in process modeling, familiar with the BPMN "
        "notation and the BPMN modelling approach. Your task is to "
        "analyze the textual description of a process and acquire a BPMN "
        "model with the help of a self-defined WorkflowProcessor class "
        "derived from PM4PY's pm4py.objects.bpmn.obj classes. When "
        "generating a model, be as precise as possible and capture all "
        "details of the process in the model. Also act as the process "
        "owner and use your expertise and familiarity with the process "
        "context to fill in any missing knowledge.\n\n"
    )


def add_knowledge():
    return (
        "Use the following knowledge about the underlying BPMN process "
        "modeling language:\n"
        " 1. Initialization:\n"
        " - Start Event: The process initiates with a Start Event, "
        "typically represented by a circle. This node marks the "
        "beginning of the process.\n"
        " 2. Task Nodes:\n"
        " - Task Definition: Following the start event, tasks are "
        "sequentially modeled as nodes. These nodes are depicted as "
        "rectangles with rounded corners. Each task represents an action "
        "or a step in the business process.\n"
        " - Examples of Tasks: These could include capturing order "
        "details, checking inventory, processing payments, or preparing "
        "shipments.\n"
        " 3. Gateway Nodes for Decision Points:\n"
        " - Inclusion of Gateways: Where the process requires "
        "decision-making or branching, gateways are used. There exists "
        "diverging and converging gateways. For this modelling task, "
        "only diverging gateways are allowed. These mark the beginning "
        "of a branching.\n"
        " - Types of Gateways:\n"
        "   - Exclusive Gateways: Used for making decisions where only "
        "     one path can be taken out of many based on conditions.\n"
        "   - Parallel Gateways: Allow multiple paths to proceed "
        "     simultaneously.\n"
        " - Gateway Handling: In the case of branches introduced by "
        "exclusive or parallel gateways, the process model will follow "
        "one branch to its end.\n"
        " 4. Modeling Sequence with Edges:\n"
        " - Connecting Nodes: Once all nodes (events, tasks, gateways) "
        "are placed, edges are drawn to connect these nodes, indicating "
        "the flow from one activity to the next.\n"
        " - Directional Flow: Arrows on the edges show the direction of "
        "the process flow. Each edge connects exactly one predecessor "
        "node to a successor node, conforming to the sequential nature of "
        "the model.\n"
        " 5. Iteration and Review:\n"
        " - Iterative Linking: The process of adding edges is iterative, "
        "ensuring that each node is properly linked to reflect the true "
        "sequence of operations in the business process.\n"
        " - Validation of Flow: As part of the modeling, it's essential "
        "to validate that the flow logically progresses from the start "
        "event, through tasks and decisions, to the conclusion of the "
        "process.\n"
        " 6. End Events:\n"
        " - Conclusion with End Event: The process concludes with an End "
        "Event, depicted as a thicker circle. This node signifies that "
        "the process has been completed, whether it ends after a task or "
        "as a result of a gateway decision.\n"
        " 7. Final Review:\n"
        " - Completeness and Correctness: The final step in the BPMN "
        "modeling process involves reviewing the entire flow for "
        "completeness and logical correctness. This includes checking "
        "that all conditional paths are accounted for and that the end "
        "events properly conclude all process threads.\n\n"
    )


def add_least_to_most():
    return (
        "Provide the Python code that sequentially models the process as "
        "a BPMN model using the class Model Generator, which is derived "
        "from PM4PY's pm4py.objects.bpmn.obj classes. In the end "
        "initialize the model with the function initialize() to check as "
        "well the model for abnormalities. First, model the nodes "
        "(Gateway, Task, Start, End) and then the edges between the nodes. "
        "Do not execute the code; just provide the plain code for external "
        "execution.\n"
        f" Assume the class WorkflowProcessor is imported using the following "
        f"statement: {IMPORT_STATEMENT} The WorkflowProcessor class offers "
        "these functions:\n"
        " - create_start_event() creates the start node object named "
        "'Start'. It takes 0 string arguments and only one start event is "
        "possible.\n"
        " - create_end_event() creates the end node object name 'End'. It "
        "takes 0 string arguments.\n"
        " - create_task(name) generates a task node object with its label "
        "name. It takes 1 string argument for the activity label.\n"
        " - create_exclusive_gateway(name) generates an exclusive diverging "
        "gateway object named after the condition's title. It takes 1 "
        "string argument. Conditions and predecessors are set later with "
        "create_exclusive_edge.\n"
        " - create_parallel_gateway(index) generates a parallel diverging "
        "gateway object for branching to multiple targets. It takes 1 "
        "arguments, which provides an index. It is not possible to create "
        "converging parallel gateways with this function.\n"
        " - create_edge(source, target) adds an edge between two nodes. It "
        "requires 2 node arguments: source and target.\n"
        " - create_exclusive_edge(source, target, condition) adds a "
        "conditional edge between an exclusive gateway and a task node. It "
        "takes 3 arguments: source node, target node, and condition. "
        "Include an opposite condition directing to the end event if "
        "there's only one condition leading to a target. Ensure all events "
        "have a successor or target. Also, note that only diverging gateways "
        "are used, no converging ones!\n\n"
    )


def add_process_description(process_description):
    return f"This is the process description to be modelled:\n" f"{process_description}"


def add_self_evaluation():
    return (
        "Avoid common mistakes. Pay attention that you indent all the code "
        "snippets to top-level. Evaluate whether one node contains more than "
        "one origin. If yes, it is likely to be a parallel stream, whereby "
        "the parallel streams contain the same task. Model the task in the "
        "parallel stream separately!\n\n"
    )


def add_output_pattern():
    return (
        "At the end of your response provide a only single Python code "
        "snippet (i.e., starting with '```python') that contains the full "
        "final code. Keep in mind to not provide explanations or unnecessary "
        "text. Also do not indent any code snippet. The code snippet should "
        "be executable as a script."
    )


def add_few_shots():
    res = "Please use few-shots learning. These are few illustrating shots.\n"
    for i, shot in enumerate(SHOTS):
        description, model = shot
        full_source = inspect.getsource(model)
        source_lines = full_source.split("\n")
        content_lines = source_lines[1:] + ["\n"]
        content_as_string = "\n".join(line[4:] for line in content_lines)

        res += f"EXAMPLE {i + 1}:\n"
        res += f"Process description for EXAMPLE {i + 1}:\n{description}\n"
        res += f"Process model for EXAMPLE {i + 1}:\n"
        res += f"```python\n{IMPORT_STATEMENT}\n{content_as_string}\n```\n\n"
    return res


def add_few_shots_with_errors():
    res = (
        "Additional to the previous few-shots, there are negative few-shots. "
        "These negative few shots contain the description of the process, "
        "the linked code and the error, why the model is not correct.\n"
    )

    for i, shot in enumerate(SHOTS_WITH_ERRORS):
        description, model, error = shot
        full_source = inspect.getsource(model)
        source_lines = full_source.split("\n")
        content_lines = source_lines[1:] + ["\n"]
        content_as_string = "\n".join(line[4:] for line in content_lines)

        res += f"EXAMPLE {i + 1}:\n"
        res += f"Process description for EXAMPLE {i + 1}:\n{description}\n"
        res += f"Process model for EXAMPLE {i + 1}:\n"
        res += f"```python\n{IMPORT_STATEMENT}\n{content_as_string}\n```\n"
        res += f"Common errors to avoid"
    return res

def create_model_generation_prompt(process_description: str) -> str:
    prompt = add_role()
    prompt = prompt + add_knowledge()
    prompt = prompt + add_least_to_most()
    prompt = prompt + add_few_shots()
    prompt = prompt + add_few_shots_with_errors()
    prompt = prompt + add_output_pattern()
    prompt = prompt + add_self_evaluation()
    prompt = prompt + add_process_description(process_description)

    return prompt
