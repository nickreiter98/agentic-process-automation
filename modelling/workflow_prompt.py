import_statement = "from modelling.generator import ModelGenerator"

def add_role():
    return "Your role: you are an expert in process modeling," \
           " familiar with common" \
           " process constructs such as exclusive and parallel gateways." \
           " Your task is to analyze the textual description of a process and transform it into a process model in" \
           " the BPMN language. When generating a model, be as precise" \
           " as possible and capture all details of the process in the model. Also act as the process owner and use" \
           " your expertise and familiarity with the" \
           " process context to fill in any missing knowledge. \n\n"


def add_knowledge():
    return " Use the following knowledge about the underlying BPMN process modeling language:\n" \
           " Our BPMN model is a sequential model and, thus, sequentially generated." \
           " By starting with the start event, the tasks are chained to its predeccesors iteratively." \
           " In case of branches like exclusive or parallel gateways, one branch is followed to the end before the " \
           " other branch is chosen." \
           " First at all the events, tasks and gateways are modeled as nodes" \
           " Subsequently the edges are added to model the sequence of the nodes." \


def add_least_to_most():
    return " Provide the Python code that " \
           " sequentially generate a BPMN model. Save the final model is the" \
           " variable 'final_model'. Do not try to execute the code, just return it. Assume the class ModelGenerator" \
           " is properly implemented and can be imported using the import statement:" \
           f" {import_statement}. ModelGenerator provides the functions" \
           " described below:\n" \
           " - start_event() creates the start node object with the name 'Start'. It takes 0 string argument \n" \
           " - end_event() creates the end node object with the name 'End'. It takes 0 string arguments \n" \
           " - task(name) generates a task node object including its label name. It takes 1 string arguments," \
           " which is the label of the activity.\n" \
           " - exclusive_gateway(name). Use this function to model and generate a exclusive gateway object" \
           " It takes 1 string argument which assigns a name to the gatway "\
           " The condition itself and the predecessors are then later provided by the function create_edge" \
           " - create_edge(origin, target) adds an edge between two nodes. It takes 2 nodes as arguments," \
           " which is the orgin and target node. Both arguments are Node objects"\
           " - create_exclusive_edge(origin, target, condition) adds an edge including condition"\
           " between an exclusive gateway and a task node. "\
           " It takes 3 arguments: the origin node, the target node, and a strink for the condition \n\n"


def add_process_description(process_description):
    return "This is the process description: " + process_description


def self_evaluation():
    return "Avoid common mistakes. " \
           "First, ensure that the transitive closure of the generated partial orders" \
           " do not violate irreflexivity. Verify that all optional/skippable and" \
           " repeatable parts are modeled correctly. Also validate that the same submodel" \
           " is not used multiple times (e.g., in xor then in partial_oder)! You have three ways for avoiding" \
           " this depending on the case: (1)" \
           " consider using loops to model cyclic behaviour; (2) if you instead want to create a second instance" \
           " of the same submodel, consider creating a copy of it; (3) if none of these two cases apply, then" \
           " your structure is not correct. Ensure that you correctly model xor/loop between larger complete" \
           " alternative/loop paths (i.e., between full paths, not decision points). Finally, do not create partial" \
           " orders as children of other partial orders. " \
           " Instead, combine dependencies at the same hierarchical level to avoid nested partial orders." \
           " Example of Correct Use of Partial Order:\n" \
           "```python\n" \
           "poset = partial_order(dependencies=[(A, B), (B, C)])\n" \
           "```\n\n" \
           "Example of Incorrect Use of Partial Order:\n" \
           "```python\n" \
           "poset_1 partial_order(dependencies=[(B, C)])\n" \
           "poset_2 = partial_order(dependencies=[(A, poset)])\n" \
           "```\n\n"


def code_generation():
    return "At the end of your response provide a only single Python code snippet (i.e., staring with '```python') that" \
           " contains the full final code. " \
           " Do not provide explanations or text\n\n"


def add_few_shots():
    process_description = 'The user has to register for the app. After registering the user can chose a product and add it to the cart. The the user is checking out and pays the product. If the payment was successfull, the product is shipped. if no, the transaction is aborted ' 
    code =  '''from modelling.generator import ModelGenerator
    
            model = ModelGenerator()

            start = model.start_event()
            register = model.task('register for app')
            chose_product = model.task('chose product')
            add_product = model.task('add product to cart')
            checkout = model.task('checkout')
            payment = model.task('payment')
            payment_successfull = model.exclusive_gateway('payment successfull')
            transaction_aborted = model.task('transaction aborted')
            start_shipping = model.task('start shipping')
            end_1 = model.end_event()
            end_2 = model.end_event()

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
            '''
 
    res = f'Process description for example {process_description}\n'
    res = res + f'Process model for example {code}:\n'
    return res + '\n'


def create_model_generation_prompt(process_description: str) -> str:
    prompt = add_role()
    prompt = prompt + add_knowledge()
    prompt = prompt + add_least_to_most()
    prompt = prompt + add_few_shots()
    prompt = prompt + code_generation()
    prompt = prompt + add_process_description(process_description)

    return prompt