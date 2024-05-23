from src.modelling.generator import ModelGenerator
                       
d1 = ("The user has to register for the app. After registering the user can"
    " chose a product and add it to the cart. The the user is checking out and pays the"
    " product. If the payment was successfull, the product is shipped. if no,"
    " the transaction is aborted.")

def m1():
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

d2 = ("Get the bank account of user 214423. Write an email to the user and"
    " also send a message to the support team.")

def m2():
    model = ModelGenerator()
    
    start = model.create_start_event()
    bank_account = model.create_task('get bank account of user 214423')
    parallel_gateway_1 = model.create_parallel_gateway('1')
    write_email = model.create_task('write email to user')
    send_message = model.create_task('send message to support team')
    end_1 = model.create_end_event()
    end_2 = model.create_end_event()

    model.create_edge(start, bank_account)
    model.create_edge(bank_account, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, write_email)
    model.create_edge(parallel_gateway_1, send_message)
    model.create_edge(write_email, end_1)
    model.create_edge(send_message, end_2)

    model.initialize()

d3 = ("Extract information from the wikipedia page about python (programming language)."
      " Then write a summary of the information. Afterwards you are sending the summary"
      " via email, Slack and also store it on your local machine. After that you are"
      " checking whether the the sending was successfull")

def m3():
    model = ModelGenerator()

    start = model.create_start_event()
    extract_info = model.create_task('extract information from wikipedia page about python')
    write_summary = model.create_task('write summary of information')
    parallel_gateway_1 = model.create_parallel_gateway('1')
    send_email = model.create_task('send summary via email')
    send_slack = model.create_task('send summary via Slack')
    store_local = model.create_task('store summary on local machine')
    check_sending_1 = model.create_task('check whether sending was successfull')
    check_sending_2 = model.create_task('check whether sending was successfull')
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

de1 = ("The user has to register for the app. After registering the user can"
    " access the app and add a product to the cart.")

def me1():
    model = ModelGenerator()

    start = model.create_start_event()
    register = model.create_task('register for app')
    access_app = model.create_task('access app')
    parallel_gateway_1 = model.create_parallel_gateway('1')
    add_product = model.create_task('add product to cart')
    end = model.create_end_event()

    model.create_edge(start, register)
    model.create_edge(register, access_app)
    model.create_edge(access_app, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, add_product)
    model.create_edge(parallel_gateway_1, end)
             
    model.initialize()

ee1 = ("This process model violates the rule that every end of a process stream"
    " must end with an end event. Also the parallel gateway is not used correctly"
    " since the workflow is clearly sequential")

de2 = ("First at all, try to get the status of user ticket 123455. Then send the"
       " status of the ticket to the user and also to the support team.")

def me2():
    model = ModelGenerator()

    start = model.create_start_event()
    get_status = model.create_task('get status of user ticket 123455')
    send_status = model.create_task('send status to user and to support team')
    end_1 = model.create_end_event()

    model.create_edge(start, get_status)
    model.create_edge(get_status, send_status)
    model.create_edge(send_status, end_1)

    model.initialize()

ee2 = ("In this process to activities are combined in one task."
       "This must be avoided under all circumstances. The proper way to "
       "to model this process is to split the task into two separate tasks"
       " and connect them with a parallel gateway.")

de3 = ("In this process, start with A. Afterwards, B is executed. After B,"
       " C and D are simultaneously executed. After C and D, E is executed.")

def me3():
    model = ModelGenerator()

    start = model.create_start_event()
    a = model.create_task('A')
    b = model.create_task('B')
    parallel_gateway_1 = model.create_parallel_gateway('1')
    c = model.create_task('C')
    d = model.create_task('D')
    e = model.create_task('E')
    end = model.create_end_event()

    model.create_edge(start, a)
    model.create_edge(a, b)
    model.create_edge(b, parallel_gateway_1)
    model.create_edge(parallel_gateway_1, c)
    model.create_edge(parallel_gateway_1, d)
    model.create_edge(c, e)
    model.create_edge(d, e)
    model.create_edge(e, end)

ee3 = ("In this process, the parallel branches are not modelled correctly."
       " After C and D, both parallel branches are converging to E."
       " Since no converging of parallel streams is possible, E must be"
       " duplicated into two edges and connected to C and D separately.")

SHOTS = [(d1, m1), (d2, m2), (d3, m3)]
SHOTS_WITH_ERRORS = [(de1, me1, ee1), (de2, me2, ee2)]