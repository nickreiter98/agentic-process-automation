from src.modelling.workflow_processor import WorkflowProcessor

# Provide the right generation of models from the textual description
d1 = (
    "The user has to register for the app. After registering the user can"
    " chose a product and add it to the cart. The the user is checking out"
    " and pays the product. If the payment was successfull, the product is"
    " shipped. if no, the transaction is aborted."
)
def m1():
    model = WorkflowProcessor()

    start = model.create_start_event()
    register = model.create_task("register for app")
    chose_product = model.create_task("chose product")
    add_product = model.create_task("add product to cart")
    checkout = model.create_task("checkout")
    payment = model.create_task("payment")
    payment_successful = model.create_exclusive_gateway("payment successful")
    transaction_aborted = model.create_task("transaction aborted")
    start_shipping = model.create_task("start shipping")
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, register)
    model.create_edge(register, chose_product)
    model.create_edge(chose_product, add_product)
    model.create_edge(add_product, checkout)
    model.create_edge(checkout, payment)
    model.create_edge(payment, payment_successful)
    model.create_exclusive_edge(payment, transaction_aborted, "payment failed")
    model.create_edge(transaction_aborted, end_2)
    model.create_exclusive_edge(
        payment_successful, start_shipping, "payment successful"
    )
    model.create_edge(start_shipping, end_1)

    model.initialize()

d2 = (
    "Get the bank account of user 214423. Write an email to the user and"
    " also send a message to the support team."
)
def m2():
    model = WorkflowProcessor()

    start = model.create_start_event()
    bank_account = model.create_task("get bank account of user 214423")
    parallel_gateway_1 = model.create_parallel_gateway("1")
    write_email = model.create_task("write email to user")
    send_message = model.create_task("send message to support team")
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, bank_account)
    model.create_edge(bank_account, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, write_email)
    model.create_edge(parallel_gateway_1, send_message)
    model.create_edge(write_email, end_1)
    model.create_edge(send_message, end_2)

    model.initialize()

d3 = (
    "Extract information from the wikipedia page about python (programming language)."
    " Then write a summary of the information. Afterwards you are sending the summary"
    " via email, Slack and also store it on your local machine. After that you are"
    " checking whether the sending was successful"
)
def m3():
    model = WorkflowProcessor()

    start = model.create_start_event()
    extract_info = model.create_task(
        "extract information from wikipedia page about python"
    )
    write_summary = model.create_task("write summary of information")
    parallel_gateway_1 = model.create_parallel_gateway("1")
    send_email = model.create_task("send summary via email")
    send_slack = model.create_task("send summary via Slack")
    store_local = model.create_task("store summary on local machine")
    check_sending_1 = model.create_task("check whether sending was successful")
    check_sending_2 = model.create_task("check whether sending was successful")
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()
    end_3 = model.create_end_event()

    model.create_edge(start, extract_info)
    model.create_edge(extract_info, write_summary)
    model.create_edge(write_summary, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, send_email)
    model.create_edge(parallel_gateway_1, send_slack)
    model.create_edge(parallel_gateway_1, store_local)
    model.create_edge(send_email, check_sending_1)
    model.create_edge(send_slack, check_sending_2)
    model.create_edge(store_local, end_1)
    model.create_edge(check_sending_1, end_2)
    model.create_edge(check_sending_2, end_3)

    model.initialize()

d4 = (
    "The process is started with A. After A, B and C are executed. After both"
    " of them D is following"
)
def m4():
    model = WorkflowProcessor()

    start = model.create_start_event()
    a = model.create_task("A")
    parallel_gateway_1 = model.create_parallel_gateway("1")
    b = model.create_task("B")
    c = model.create_task("C")
    d1 = model.create_task("D")
    d2 = model.create_task("D")
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, a)
    model.create_edge(a, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, b)
    model.create_edge(parallel_gateway_1, c)
    model.create_edge(b, d1)
    model.create_edge(c, d2)
    model.create_edge(d1, end_1)
    model.create_edge(d2, end_2)

    model.initialize()

d5 = (
    "Get a. Check whether a is a large number. If a is larger than 25 send a message"
    ", if not, break the process."
)

def m5():
    model = WorkflowProcessor()

    start = model.create_start_event()
    get_a = model.create_task("get a")
    check_a = model.create_task("check whether a is a large number")
    send_message = model.create_task("send message")
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, get_a)
    model.create_edge(get_a, check_a)
    model.create_exclusive_edge(check_a, send_message, "a > 25")
    model.create_exclusive_edge(check_a, end_2, "a <= 25")
    model.create_edge(send_message, end_1)

    model.initialize()

# Provide examples which would lead to errors during model generation.
# Also provide the error explanation
de1 = (
    "First, register for the app. Then access the app. After that, add a"
    " product to the cart."
)
def me1():
    model = WorkflowProcessor()

    start = model.create_start_event()
    register = model.create_task("register for app")
    access_app = model.create_task("access app")
    parallel_gateway_1 = model.create_parallel_gateway("1")
    add_product = model.create_task("add product to cart")
    end = model.create_end_event()

    model.create_edge(start, register)
    model.create_edge(register, access_app)
    model.create_edge(access_app, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, add_product)
    model.create_edge(parallel_gateway_1, end)

    model.initialize()
ee1 = (
    "This process model violates the rule that every end of a process stream"
    " must end with an end event. Also the parallel gateway is not used correctly"
    " since the workflow is clearly sequential"
)

de2 = (
    "First at all, try to get the status of user ticket 123455. Then send the"
    " status of the ticket to the user and also to the support team."
)
def me2():
    model = WorkflowProcessor()

    start = model.create_start_event()
    get_status = model.create_task("get status of user ticket 123455")
    send_status = model.create_task("send status to user and to support team")
    end_1 = model.create_end_event()

    model.create_edge(start, get_status)
    model.create_edge(get_status, send_status)
    model.create_edge(send_status, end_1)

    model.initialize()
ee2 = (
    "In this process two activities are combined in one task. This must be"
    " avoided under all circumstances. The proper way to model this process"
    " is to split the task into two separate tasks and connect them with a"
    " parallel gateway."
)

de3 = (
    "In this process, start with A. Afterwards, B is executed. After B, C and"
    " D are simultaneously executed. After C and D, E is executed."
)
def me3():
    model = WorkflowProcessor()

    start = model.create_start_event()
    a = model.create_task("A")
    b = model.create_task("B")
    parallel_gateway_1 = model.create_parallel_gateway("1")
    c = model.create_task("C")
    d = model.create_task("D")
    e = model.create_task("E")
    end = model.create_end_event()

    model.create_edge(start, a)
    model.create_edge(a, b)
    model.create_edge(b, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, c)
    model.create_edge(parallel_gateway_1, d)
    model.create_edge(c, e)
    model.create_edge(d, e)
    model.create_edge(e, end)
ee3 = (
    "In this process, the parallel branches are not modelled correctly."
    " After C and D, both parallel branches are converging to E. Since no"
    " converging of parallel streams is possible, E must be duplicated into"
    " two edges and connected to C and D separately."
)

de4 = (
    "Firstly, A is triggered. A is followed by B. To end the process, C and"
    " D are triggered"
)
def me4():
    model = WorkflowProcessor()

    start = model.create_start_event()
    a = model.create_task("A")
    b = model.create_task("B")
    parallel_gateway_1 = model.create_parallel_gateway("1")
    c = model.create_task("C")
    parallel_gateway_1a = model.create_parallel_gateway("1a")
    d = model.create_task("D")
    parallel_gateway_1b = model.create_parallel_gateway("1b")
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, a)
    model.create_edge(a, b)
    model.create_edge(b, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, c)
    model.create_edge(parallel_gateway_1, d)
    model.create_edge(c, parallel_gateway_1a)
    model.create_edge(d, parallel_gateway_1b)
    model.create_edge(parallel_gateway_1a, end_1)
    model.create_edge(parallel_gateway_1b, end_2)

    model.initialize()
ee4 = (
    "In this process, the parallel gateways '1a' and '1b' are not used"
    " correctly. Normally, parallel gateways are used for diverging a process"
    " stream. In this case, the parallel gateways are unnecessary and can be"
    " removed. Also, an end event must follow a task and not a parallel or"
    " exclusive gateway."
)

de5 = (
    "Get the current water level of the Rhine. Check if the water how high "
    "the water level is. If it is higher than 100cm send a message to "
    "nick.reiter@hotmail.de. if lower than 100cm, break the process."
)

def me5():
    model = WorkflowProcessor()

    start = model.create_start_event()
    get_water_level = model.create_task("get current water level of the Rhine")
    check_water_level = model.create_task("check how high water level is")
    high_water_level = model.create_exclusive_gateway("water level is high or not")
    send_message = model.create_task("send message to nick.reiter@hotmail.de")
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, get_water_level)
    model.create_edge(get_water_level, check_water_level)
    model.create_edge(check_water_level, high_water_level)
    model.create_exclusive_edge(high_water_level, send_message, "water level > 100cm")
    model.create_exclusive_edge(high_water_level, end_2, "water level <= 100cm")
    model.create_edge(send_message, end_1)

    model.initialize()

ee5 = (
    "In this process, the exclusive gateway is not used correctly "
    "The exclusive gateway must represent the decision-making respectively "
    "the business rule of the process. In this case the exclusive gateway "
    "is separated in 'check how high water level is' and 'water level is high or not'. "
    "Since both relate to decision-making, they must be combined in one exclusive gateway."
)

SHOTS = [(d1, m1), (d2, m2), (d3, m3), (d4, m4), (d5, m5)]
SHOTS_WITH_ERRORS = [
    (de1, me1, ee1), (de2, me2, ee2), (de3, me3, ee3), (de4, me4, ee4), (de5, me5, ee5)
]
