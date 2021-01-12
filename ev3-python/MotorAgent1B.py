from MotorAgent import MotorAgent
import spade
from MyBehaviour import CyclicBehaviour, OneShotBehaviour
import time
import agentnames

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
			self.turnOffRotation = 0
			self.buildCount = 0
			self.firstStuckCall = True
		async def shred(self):
			await self.logInfo("Agent1B::shred -> resetRotation & setSpeed(10)")
			self.agent.resetRotation()
			await self.agent.runDegs(790, -30)

		async def brickStuck(self):
			await self.logInfo("Agent1B::brickStuck start")
			if not self.firstStuckCall:
				print("brick stuck unstucking")
				await self.agent.runDegs(100, 20)
				self.agent.resetRotation()
				await self.agent.runDegs(790, -30)
			else:
				self.firstStuckCall = False
			previousRotation = self.agent.readRotation()
			while (abs(self.agent.readRotation()) < 780):
				print(f"brick stuck sleeping! Current: {self.agent.readRotation()}")
				await self.agent.sleep(1)
				if previousRotation == self.agent.readRotation():
					msg = spade.message.Message()
					msg.to = agentnames.error
					msg.body = f'Something went wrong with the {self.agent.jid} rotation control.'
					await self.send(msg)
					await self.logInfo("Agent1B encountered a bit of a problem. Sleeping for ten seconds, will assume fixed after.")
			# Wait with sending this message until the brick should actually be there.
			await self.agent.sleep(2)
			msg = spade.message.Message()
			msg.to = agentnames.agent14
			msg.body = 'no stuck brick'
			await self.send(msg)
			await self.logInfo("Agent1B::brickStuck end")

		async def brickArrival(self):
			await self.logInfo("Agent1B::brickArrival -> float()")
			self.agent.port.float()
			self.firstStuckCall = True # We go past that stage, so fix the variable for next time

		async def barrierOn(self):
			await self.logInfo("Agent1B::barrierOn -> float()")
			self.turnOffRotation = self.agent.readRotation()
			self.agent.port.float()
		
		async def barrierOff(self):
			await self.logInfo("Agent1B::barrierOff -> setSpeed(10)")
			await self.agent.runDegs(780 - self.turnOffRotation, -30)
			self.turnOffRotation = 0

		async def build(self):
			await self.logInfo("Agent1B::build start")
			await self.agent.runDegs(degs=1800, speed=-30, brakeOnCompletion=False)
			self.buildCount += 1
			msg = spade.message.Message()
			msg.body = str(self.buildCount)
			msg.metadata = {"parameter": "press"}
			msg.thread = "1"
			msg.to = agentnames.agent2D
			await self.send(msg)
			self.buildCount %= 2
			await self.logInfo("Agent1B::build end")

		async def sort(self, bucketIndex):
			await self.logInfo("Agent1B::sort start")
			degValues = {0: 400, 1: 600, 2: 850}
			await self.agent.runDegs(degs=degValues[bucketIndex], speed=-30, brakeOnCompletion=True)
			msg = spade.message.Message()
			msg.body = 'brick sorted'
			msg.to = agentnames.agent2C
			await self.send(msg)
			await self.logInfo("Agent1B::sort end")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = "1B"
		self.add_behaviour(self.Behaviour())

	

def createAgent1B():
	return MotorAgent1B(agentnames.agent1B, "agent1B")
