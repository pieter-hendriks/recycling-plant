from MotorAgent import MotorAgent
import time
import spade
from MyBehaviour import CyclicBehaviour, OneShotBehaviour
class MotorAgent2B(MotorAgent):
	class Behaviour_start(OneShotBehaviour): 
		async def run(self): # R_EJT
			self.agent.port.setSpeed(-8)
			time.sleep(1)
			self.agent.port.waitUntilNotBusy()
			self.agent.port.brake()
			self.agent.resetRotation()
			self.agent.port.float()
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.eject))
			self.templates[-1][0].body = 'eject'
			self.createMasterTemplate()
		
		async def eject(self, count=2):
			for _ in range(count):
				self.agent.resetRotation()
				self.agent.port.runSecs(secs=0.6, speed=30, brakeOnCompletion=True)
				time.sleep(0.6)
				degs=10-self.agent.readRotation()
				self.agent.port.runDegs(degs=degs, speed=-50, brakeOnCompletion=True)
				time.sleep(1)
			msg = spade.message.Message()
			msg.to = 'agent11@192.168.1.8'
			msg.body = 'next brick'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = 'out@192.168.1.8'
			msg.body = 'next brick'
			await self.send(msg)

	def __init__(self, *args, **kwargs):
		# Forward all arguments to super since we don't really use any ourselves.
		super().__init__(*args, **kwargs)
		self.add_behaviour(self.Behaviour_start())
		self.add_behaviour(self.Behaviour())
		self.agentname = "2B"

	

def createAgent2B():
	return MotorAgent2B("agent2B@192.168.1.8", "agent2B")