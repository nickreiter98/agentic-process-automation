import_statement = "from modelling.generator import ModelGenerator"

def add_role():
    return " Act as an expert in process modeling, familiar with the BPMN notation and "\
            " the BPMN modelling approach. Your task is to analyze the textual description of a "\
            " and acquire a BPMN model with the help of a self-defined ModelGenerator class derived from PM4PY's pm4py.objects.bpmn.obj classes. When "\
            " generating a model, be as precise as possible and capture all details of the "\
            " process in the model. Also act as the process owner and use your expertise and "\
            " familiarity with the process context to fill in any missing knowledge."


def add_knowledge():
    return " Use the following knowledge about the underlying BPMN process modeling language:\n\n" \
            " 1. Initialization:\n" \
            " - Start Event: The process initiates with a Start Event, typically " \
            " represented by a circle. This node marks the beginning of the process.  \n\n" \
            " 2. Task Nodes:\n" \
            " - Task Definition: Following the start event, tasks are sequentially"\
            " modeled as nodes. These nodes are depicted as rectangles with rounded corners."\
            " Each task represents an action or a step in the business process.\n"\
            " - Examples of Tasks: These could include capturing order details, checking"\
            " inventory, processing payments, or preparing shipments.\n\n"\
            " 3. Gateway Nodes for Decision Points:\n"\
            " - Inclusion of Gateways: Where the process requires decision-making or"\
            " branching, gateways are used. These are represented as diamond shapes.\n"\
            " - Types of Gateways:\n"\
            "   - Exclusive Gateways: Used for making decisions where only one path can"\
            "     be taken out of many based on conditions.\n"\
            "   - Parallel Gateways: Allow multiple paths to proceed simultaneously.\n"\
            " - Sequential Branch Handling: In the case of branches introduced by exclusive \n"\
            " or parallel gateways, the process model will follow one branch to its conclusion"\
            " before backtracking to explore another branch. This is handled sequentially in"\
            " modeling, ensuring clarity and order in the process flow.\n\n"\
            " 4. Modeling Sequence with Edges:\n"\
            " - Connecting Nodes: Once all nodes (events, tasks, gateways) are placed, edges"\
            " are drawn to connect these nodes, indicating the flow from one activity to the"\
            " next.\n"\
            " - Directional Flow: Arrows on the edges show the direction of the process"\
            " flow. Each edge connects exactly one predecessor node to a successor node,"\
            " conforming to the sequential nature of the model.\n\n"\
            " 5. Iteration and Review:\n"\
            " - Iterative Linking: The process of adding edges is iterative, ensuring that"\
            " each node is properly linked to reflect the true sequence of operations in the"\
            " business process.\n"\
            " - Validation of Flow: As part of the modeling, it's essential to validate"\
            " that the flow logically progresses from the start event, through tasks and"\
            " decisions, to the conclusion of the process.\n\n"\
            " 6. End Events:\n"\
            " - Conclusion with End Event: The process concludes with an End Event,"\
            " depicted as a thicker circle. This node signifies that the process has been"\
            " completed, whether it ends after a task or as a result of a gateway decision.\n\n"\
            " 7. Final Review:\n"\
            " - Completeness and Correctness: The final step in the BPMN modeling process"\
            " involves reviewing the entire flow for completeness and logical correctness. This"\
            " includes checking that all conditional paths are accounted for and that the end"\
            " events properly conclude all process threads."

def add_least_to_most():
    return " Provide the Python code that sequentially models the process as a BPMN model using the "\
            " class Model Generator, which is derived from PM4PY's pm4py.objects.bpmn.obj classes."\
            " In the end intialize the model with the function initialize() to check as well the model for abnormalities. First,"\
            " model the nodes (Gateway, Task, Start, End) and then the edges between the nodes. Do not "\
            " execute the code; just provide the plain code for external execution.\n"\
            f" Assume the class ModelGenerator is imported using the following statement: {import_statement}"\
            " The ModelGenerator class offers these functions:\n"\
            " - create_start_event() creates the start node object named 'Start'. It takes 0 string "\
            " arguments and only one start event is possible.\n"\
            " - create_end_event() creates the end node object named 'End'. It takes 0 string arguments.\n"\
            " - create_task(name) generates a task node object with its label name. It takes 1 string "\
            " argument for the activity label.\n"\
            " - create_exclusive_gateway(name) generates an exclusive diverging gateway object named after the "\
            " condition's title. It takes 1 string argument. Conditions and predecessors are set later with "\
            " create_exclusive_edge.\n"\
            " - create_parallel_gateway(index) generates a parallel diverging gateway object for branching to multiple "\
            " targets. It takes 1 arguments, which provides an index.\n"\
            " - create_edge(source, target) adds an edge between two nodes. It requires 2 node arguments: "\
            " source and target.\n"\
            " - create_exclusive_edge(source, target, condition) adds a conditional edge between an "\
            " exclusive gateway and a task node. It takes 3 arguments: source node, target node, and "\
            " condition. Include an opposite condition directing to the end event if there's only one "\
            " condition leading to a target. Ensure all events have a successor or target. Also, "\
            " note that only diverging gateways are used, no converging ones!\n\n"\


def add_process_description(process_description):
    return " This is the process description: " + process_description


def self_evaluation():
    return " Avoid common mistakes. " \
           " pay attention that you indent all the code snippets to top-level."\
           " Evaluate wheter one node contains more than one origin. If yes,"\
           " it is likely to be a parallel stream, whereby the parallel streams"\
           " contain the same task. Model the task in the parallel stream separately!"


def code_generation():
    return " At the end of your response provide a only single Python code snippet (i.e., staring with '```python') that" \
           " contains the full final code. Keep in mind to " \
           " not provide explanations or unnecessary text\n\n"


def add_few_shots():
    process_description = [" The user has to register for the app. After registering the user can"\
                           " chose a product and add it to the cart. The the user is checking out and pays the"\
                           " product. If the payment was successfull, the product is shipped. if no,"\
                           " the transaction is aborted ",
                           " Get the bank account of user 214423. Write an email to the user and also send a"\
                           " message to the support team."] 
    code =  ["""```python
    from modelling.generator import ModelGenerator

    model = ModelGenerator()

    start = model.create_start_event()
    register = model.create_task('register for app')
    chose_product = model.create_task('chose product')
    add_product = model.create_task('add product to cart')
    checkout = model.create_task('checkout')
    payment = model.create_task('payment')
    payment_successfull = model.create_exclusive_gateway('payment successfull')
    transaction_aborted = model.create_task('transaction aborted')
    start_shipping = model.create_task('start shipping')
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, register)
    model.create_edge(register, chose_product)
    model.create_edge(chose_product, add_product)
    model.create_edge(add_product, checkout)
    model.create_edge(checkout, payment)
    model.create_edge(payment, payment_successfull)
    model.create_exclusive_edge(payment, transaction_aborted, 'payment failed')
    model.create_edge(transaction_aborted, end_2)
    model.create_exclusive_edge(payment_successfull, start_shipping, 'payment successfull')
    model.create_edge(start_shipping, end_1)
             
    model.initialize()
            ```""",
            """```python
    from modelling.generator import ModelGenerator
    
    model = ModelGenerator()
    
    start = model.create_start_event()
    bank_account = model.create_task('get bank account of user 214423')
    parallel_gateway_1 = model.create_parallel_gateway('1')
    write_email = model.create_task('write email to user')
    send_message = model.create_task('send message to support team')
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, bank_account)
    model.create_edge(bank_account, parallel_gateway)
    model.create_edge(parallel_gateway_1, write_email)
    model.create_edge(parallel_gateway_1, send_message)
    model.create_edge(write_email, end_1)
    model.create_edge(send_message, end_2)

    model.initialize()
            ```"""
        ]
    
    res = ''
    for i in range(len(process_description)):
        res = res + f'EXAMPLE {i+1}:\n'
        res = res + f'Process description for example {process_description[i]}\n'
        res = res + f'Process model for example {code[i]}:\n\n'
    return res + '\n'


def create_model_generation_prompt(process_description: str) -> str:
    prompt = add_role()
    prompt = prompt + add_knowledge()
    prompt = prompt + add_least_to_most()
    prompt = prompt + add_few_shots()
    prompt = prompt + code_generation()
    prompt = prompt + self_evaluation()
    prompt = prompt + add_process_description(process_description)

    return prompt