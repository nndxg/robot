from iexfinance import Stock
from iexfinance import get_market_tops
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

# Create a trainer that uses this config
trainer = Trainer(config.load("config_spacy.yml"))

# Load the training data
training_data = load_data('demo-rasa.json')

# Create an interpreter by training the model
interpreter = trainer.train(training_data)

def send_message(policy, state, message):
	print("USER : {}".format(message))
	new_state, response = respond(policy, state, message)
	print("BOT : {}".format(response))
	return new_state

def respond(policy, state, message):
	entities = interpreter.parse(message)["entities"]
	print(entities)
	(new_state, response) = policy[(state, interpret(message))]
	return new_state, response

def interpret(message):
	msg = message.lower()
	if 'stock' in msg:
		return 'stock'
	if 'tsla' in msg or 'columbian' in msg:
		return 'specify_stock'
	if 'price' in msg or 'columbian' in msg:
		return 'specify_function'
	if 'yes' in msg:
		return 'yes'
	if 'no' in msg:
		return 'no'
	return 'none'


INIT = 0
ASK_STOCK = 1
ASKING = 2
ASKED = 3
OVER = 4


# Define the policy rules
policy = {
	(INIT, "stock"): (ASK_STOCK, "Which stock do you want to ask?"),
	(INIT, "specify_stock"): (INIT, "I'm sorry - I'm not sure how to help you"),
	(INIT, "specify_function"): (INIT, "I'm sorry - I'm not sure how to help you"),
	(INIT, "yes"): (INIT, "I'm sorry - I'm not sure how to help you"),
	(INIT, "no"): (INIT, "I'm sorry - I'm not sure how to help you"),
	(INIT, "none"): (INIT, "I'm sorry - I'm not sure how to help you"),

	(ASK_STOCK, "specify_stock"): (ASKING, "what do you want to know about this stock?"),
	(ASK_STOCK, "stock"): (ASK_STOCK, "I'm sorry - which stock do you want to ask?"),
	(ASK_STOCK, "specify_function"): (ASK_STOCK, "I'm sorry - which stock do you want to ask?"),
	(ASK_STOCK, "yes"): (ASK_STOCK, "I'm sorry - which stock do you want to ask?"),
	(ASK_STOCK, "no"): (ASK_STOCK, "I'm sorry - which stock do you want to ask?"),
	(ASK_STOCK, "none"): (ASK_STOCK, "I'm sorry - which stock do you want to ask?"),

	(ASKING, "specify_function"): (ASKED, "perfect, do you want to ask something else?"),
	(ASKING, "stock"): (ASKING, "I'm sorry - this function is not included?"),
	(ASKING, "specify_stock"): (ASKING, "I'm sorry - this function is not included?"),
	(ASKING, "yes"): (ASKING, "I'm sorry - this function is not included?"),
	(ASKING, "no"): (ASKING, "I'm sorry - this function is not included?"),
	(ASKING, "none"): (ASKING, "I'm sorry - this function is not included?"),

	(ASKED, "yes"): (INIT, "you can ask something else"),
	(ASKED, "no"): (OVER, "Thank you"),
	(ASKED, "stock"): (ASKED, "I'm sorry - do you want to ask something else?"),
	(ASKED, "specify_stock"): (ASKED, "I'm sorry - do you want to ask something else?"),
	(ASKED, "specify_function"): (ASKED, "I'm sorry - do you want to ask something else?"),
	(ASKED, "none"): (ASKED, "I'm sorry - do you want to ask something else?"),
	
	(OVER, "stock"): (OVER, "It's over, Thank you"),
	(OVER, "specify_stock"): (OVER, "It's over, Thank you"),
	(OVER, "specify_function"): (OVER, "It's over, Thank you"),
	(OVER, "yes"): (OVER, "It's over, Thank you"),
	(OVER, "no"): (OVER, "It's over, Thank you"),
	(OVER, "none"): (OVER, "It's over, Thank you"),

}

# Create the list of messages
messages = []

# Call send_message() for each message
state = INIT
for message in messages:    
	state = send_message(policy, state, message)
