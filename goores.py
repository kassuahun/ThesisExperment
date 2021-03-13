#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from math import exp
from time import sleep

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#########################################################################################################################


# Here you can try different parameters and see how it affects the run.

GROWTH_VECTOR = 0.2 	# How much each reward changes behaviour
TARGET = 0.7			# How many yes-nodes we want, divided by 10
ROUND_THRESHOLD = 10	# How many succesive iterations to pass with correct value before system is regarded as optimal
'''

	What we need to optimise, ..... 
	How to determn the treshold 
	Can we use the same thing with variable NODE ?

'''
NODES = 10				# How many voters we want in our system
DELAY = 0.1				# How many seconds to sleep between iterations (might be good for viewing algorithm in action)
LIMIT = 1000			# If algorithm gets stuck on a reward loop close to the TARGET, we can break


#########################################################################################################################

C = Color()
class Voter():
	
	p1 = 0.5
	p2 = 0.5
	yes = True

	def vote(self):
		if random.random() < self.p1:
			self.yes = True
		else:
			self.yes = False
		return self.yes

	def reward(self, vector):
		if random.random() < vector:
			if self.yes:
				self.p1 = self.p1 + GROWTH_VECTOR*(1-self.p1)
				self.p2 = 1 - self.p1
				return True
			else:
				self.p2 = self.p2 + GROWTH_VECTOR*(1-self.p2)
				self.p1 = 1 - self.p2
				return False

	def __str__(self):
		retstr = str(self.yes)+": p1: "+str(self.p1)+" | p2: "+str(self.p2)
		return retstr

class Referee():
	
	voterlist = []

	def __init__(self, voter_amount):
		for x in range(0,voter_amount):
			self.voterlist.append(Voter())

	def count_votes(self):
		votes = 0
		for voter in self.voterlist:
			if voter.vote(): #if the vote is yes
				votes = votes+1
		return float(votes) / float(len(self.voterlist))

	def judge(self, votes):
		return 0.9 * exp(-(TARGET-votes)*(TARGET-votes)/0.0625)

	def loop_once(self):
		votes = self.count_votes()
		threshold = self.judge(votes)
		for voter in self.voterlist:
			if voter.reward(threshold):
				print(C.OKGREEN+str(voter)+C.ENDC)
			else:
				print(str(voter))
		print("\n\t\t"+C.WARNING+str(votes*10)+C.ENDC)
		return votes

ref = Referee(NODES)
round_count = 0
count = 0
generation = 0

while (True):
	#print("\033c") # Clear console (Linux)
	print("GENERATION: "+str(generation)+"\n\n")
	generation = generation+1
	if ref.loop_once() == TARGET:
		count = count+1
	else:
		count = 0
	sleep(DELAY)
	round_count = round_count+1
	if count > ROUND_THRESHOLD:
		print("\n"+C.UNDERLINE+"Target reached "+str(ROUND_THRESHOLD)+" times in succession, system optimized\n"+C.ENDC)
		break
	if round_count > LIMIT:
		print(C.FAIL+"LIMIT reached"+C.ENDC)
		break