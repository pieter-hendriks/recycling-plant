import spade
from MyBehaviour import ControlBehaviour
import asyncio
import time

class MyAgent(spade.agent.Agent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# PiStorm and MotorPort variables, set in setup 
		self.psm = None 
		self.port = None
		self.agentname = "UNINITIALIZED"
		self.nextValue = None
		self.add_behaviour(ControlBehaviour())
		self.holdConfiguredValue = False

	def setNextMeasurementValue(self, value, hold):
		print ("Controller setting next measurement value!")
		self.nextValue = value
		self.holdConfiguredValue = hold

	async def sleep(self, t):
		await asyncio.sleep(t) #asyncio.wait_for(self.__sleep(t), timeout=t+2)

	#async def __sleep(self, t):
	#	time.sleep(t)
	#	return 

