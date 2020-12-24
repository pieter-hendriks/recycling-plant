from MyAgent import MyAgent
from PiStorms import PiStorms, PiStormsMotor
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template




class MotorAgent(MyAgent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Bandaid fix because system doesn't expose resetRotation
		self.rotationOffset = 0
		
	def __getPort(self):
		assert self.agentname is not None
		if self.agentname[1] == "A":
			return self.psm.BAM1
		elif self.agentname[1] == "B":
			return self.psm.BAM2
		elif self.agentname[1] == "C":
			return self.psm.BBM1
		elif self.agentname[1] == "D":
			return self.psm.BBM2

	def readRotation(self):
		return self.port.pos() - self.rotationOffset
	def resetRotation(self):
		self.rotationOffset = self.port.pos()

	async def setup(self):
		await super().setup()
		print(f"Hi! I'm MotorAgent {self.agentname}, with id {self.jid}.")
		self.psm :PiStorms = PiStorms()
		self.port :PiStormsMotor = self.__getPort()
