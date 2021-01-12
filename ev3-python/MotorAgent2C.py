from MotorAgent import MotorAgent
import time
from MyBehaviour import OneShotBehaviour, CyclicBehaviour
import spade
import agentnames

class MotorAgent2C(MotorAgent):
	class Behaviour_start(OneShotBehaviour):
		async def run(self): # R_SRT
			await self.logInfo("agent2C::run start")
			await self.agent.runSecs(secs=2, speed=10, brakeOnCompletion=True)
			await self.agent.sleep(0.1)
			self.agent.port.float()
			self.agent.resetRotation()
			await self.logInfo("agent2C::run end")
		
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.push))
			self.templates[-1][0].body = 'brick sorted'
			self.createMasterTemplate()
		async def push(self):
			await self.logInfo("agent2C::push start")
			degs = 80 - self.agent.readRotation()
			await self.agent.runDegs(degs=degs, speed=-20, brakeOnCompletion=True)
			await self.agent.sleep(0.3)
			degs = 5 - self.agent.readRotation()
			await self.agent.runDegs(degs=degs, speed=20, brakeOnCompletion=True)
			await self.agent.sleep(0.2)
			self.agent.port.float()
			msg = spade.message.Message()
			msg.to = agentnames.agent11
			msg.body = 'ready'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = agentnames.output
			msg.body = 'ready'
			await self.send(msg)
			await self.logInfo("agent2C::push end")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = "2C"
		self.add_behaviour(self.Behaviour_start())
		self.add_behaviour(self.Behaviour())

		


def createAgent2C():
	return MotorAgent2C(agentnames.agent2C, "agent2C")
