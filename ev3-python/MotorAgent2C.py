from MotorAgent import MotorAgent
import time
from MyBehaviour import OneShotBehaviour, CyclicBehaviour
import spade


class MotorAgent2C(MotorAgent):
	class Behaviour_start(OneShotBehaviour):
		async def run(self): # R_SRT
			self.agent.port.setSpeed(-8)
			time.sleep(0.3)
			#self.agent.port.waitUntilNotBusy()
			self.agent.port.brake()
			self.agent.resetRotation()
			self.agent.port.float()
		
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.push))
			self.templates[-1][0].body = 'brick sorted'
			self.createMasterTemplate()
		async def push(self):
			degs = 80 - self.agent.readRotation()
			self.agent.port.runDegs(degs=degs, speed=40, brakeOnCompletion=True)
			time.sleep(0.3)
			degs = 5 - self.agent.readRotation()
			self.agent.port.runDegs(degs=degs, speed=40, brakeOnCompletion=True)
			time.sleep(0.2)
			self.agent.port.hold()
			msg = spade.message.Message()
			msg.to = 'agent11@192.168.1.8'
			msg.body = 'next brick'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = 'output@192.168.1.8'
			msg.body = 'next brick'
			await self.send(msg)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = "2C"
		self.add_behaviour(self.Behaviour_start())
		self.add_behaviour(self.Behaviour())

		


def createAgent2C():
	return MotorAgent2C("agent2C@192.168.1.8", "agent2C")
