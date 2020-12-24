import spade

class MyAgent(spade.agent.Agent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# PiStorm and MotorPort variables, set in setup
		self.psm = None 
		self.port = None
		self.agentname = "UNINITIALIZED"
