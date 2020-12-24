from MotorAgent import MotorAgent
import spade
from MyBehaviour import CyclicBehaviour, OneShotBehaviour
class MotorAgent1B(MotorAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.shred))
			self.templates[-1][0].body = "brick dropped"
			self.templates.append((spade.template.Template(), self.brickStuck))
			self.templates[-1][0].body = "maybe stuck"
			self.templates.append((spade.template.Template(), self.brickArrival))
			self.templates[-1][0].body = "brick arrived"
			self.templates.append((spade.template.Template(), self.barrierOn))
			self.templates[-1][0].body = "proximity alert"
			self.templates.append((spade.template.Template(), self.barrierOff))
			self.templates[-1][0].body = "area clear"
			self.templates.append((spade.template.Template(), self.build))
			self.templates[-1][0].body = "build"
			self.templates.append((spade.template.Template(), self.sort))
			self.templates[-1][0].metadata = {"parameter": "sort"}
			self.templates[-1][0].thread = "1"
			self.createMasterTemplate()

			self.buildCount = 0

		async def shred(self):
			self.agent.resetRotation()
			self.agent.port.setSpeed(10)

		async def brickStuck(self):
			if (self.agent.readRotation() > 1200):
				self.agent.port.runSecs(secs=1, speed=-20, brakeOnCompletion=True)
				self.agent.resetRotation()
				self.agent.port.setSpeed(10)
			msg = spade.message.Message()
			msg.to = 'agent14@192.168.1.8'
			msg.body = 'no stuck brick'
			await self.send(msg)

		async def brickArrival(self):
			self.agent.port.float()

		async def barrierOn(self):
			self.agent.port.float()
		
		async def barrierOff(self):
			self.agent.port.setSpeed(10)

		async def build(self):
			self.agent.port.runDegs(degs=1600, speed=30, brakeOnCompletion=False)
			self.buildCount += 1
			msg = spade.message.Message()
			msg.body = str(self.buildCount)
			msg.metadata = {"parameter": "press"}
			msg.thread = "1"
			msg.to = 'agent2D@192.168.1.8'
			await self.send(msg)

			self.buildCount %= 2

		async def sort(self, bucketIndex):
			degValues = {0: 390, 1: 630, 2: 870}
			self.agent.port.runDegs(degs=degValues[bucketIndex], speed=20, brakeOnCompletion=True)
			msg = spade.message.Message()
			msg.body = 'brick sorted'
			msg.to = 'agent2C@192.168.1.8'
			await self.send(msg)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = "1B"
		self.add_behaviour(self.Behaviour())

	

def createAgent1B():
	return MotorAgent1B("agent1B@192.168.1.8", "agent1B")
