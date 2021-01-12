from MotorAgent import MotorAgent
import spade
from MyBehaviour import CyclicBehaviour
import agentnames 
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
			await self.logInfo("Agent1C::brickArrival -> port.hold()")
			self.agent.port.brake()
			self.agent.port.float()

		async def shred(self):
			await self.logInfo("Agent1C::shred -> setSpeed(70)")
			self.agent.port.setSpeed(20)

		async def barrierOn(self):
			self.agent.port.float()
		
		async def barrierOff(self):
			self.agent.port.setSpeed(20)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = "1C"
		self.add_behaviour(self.Behaviour())


def createAgent1C():
	return MotorAgent1C(agentnames.agent1C, "agent1C")