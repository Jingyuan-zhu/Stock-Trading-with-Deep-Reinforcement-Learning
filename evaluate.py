import keras
from keras.models import load_model
import tensorflow as tf
from agent.agent import Agent
from functions import *
import sys

if len(sys.argv) != 3:
	print ("Usage: python evaluate.py [stock] [model]")
	exit()

stock_name, model_name = sys.argv[1], sys.argv[2]
# model = tf.saved_model.load("models/model_ep0/" + model_name)
model = load_model(model_name)
window_size = list(model.layers[0].input.shape)[1]
agent = Agent(window_size, True, model_name)
data = getStockDataVec(stock_name)
l = len(data) - 1 # in our case, the unit will be in miliseconds
batch_size = 32

state = getState(data, 0, window_size + 1)
total_profit = 0
agent.inventory = []

for t in range(l):
	action = agent.act(state)

	# sit
	next_state = getState(data, t + 1, window_size + 1)
	reward = 0

	if action == 1: # buy
		agent.inventory.append(data[t])
		print ("Buy: " + formatPrice(data[t]))

	elif action == 2 and len(agent.inventory) > 0: # sell
		bought_price = agent.inventory.pop(0)
		reward = max(data[t] - bought_price, 0)
		total_profit += data[t] - bought_price
		print ("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))

	done = True if t == l - 1 else False
	agent.memory.append((state, action, reward, next_state, done))
	state = next_state

	if done:
		print ("--------------------------------")
		print (stock_name + " Total Profit: " + formatPrice(total_profit))
		print ("--------------------------------")
