from MotorAgent import MotorAgent
import spade
from MyBehaviour import CyclicBehaviour

class MotorAgent1C(MotorAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.brickArrival))
			self.templates[-1][0].body = 'brick arrived'
			self.templates.append((spade.template.Template(), self.shred))
			self.templates[-1][0].body = 'brick dropped'
			self.templates.append((spade.template.Template(), self.barrierOn))
			self.templates[-1][0].body = 'proximity alert'
			self.templates.append((spade.template.Template(), self.barrierOff))
			self.templates[-1][0].body = 'area clear'
			self.createMasterTemplate()
	
		async def brickArrival(self):
			self.agent.port.hold()

		async def shred(self):
			self.agent.port.setSpeed(70)

		async def barrierOn(self):
			self.agent.port.float()
		
		async def barrierOff(self):
			self.agent.port.setSpeed(70)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = "1C"
		self.add_behaviour(self.Behaviour())


def createAgent1C():
	return MotorAgent1C("agent1C@192.168.1.8", "agent1C")