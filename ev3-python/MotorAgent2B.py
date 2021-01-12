from MotorAgent import MotorAgent
import time
import spade
from MyBehaviour import CyclicBehaviour, OneShotBehaviour
import agentnames 

class MotorAgent2B(MotorAgent):
	class Behaviour_start(OneShotBehaviour): 
		async def run(self): # R_EJT
			await self.logInfo("agent2B::run start")
			await self.agent.runSecs(speed=10, secs=1, brakeOnCompletion=True)
			await self.agent.runSecs(speed=40, secs=0.5, brakeOnCompletion=True)
			self.agent.resetRotation()
			await self.logInfo("agent2B::run end")

	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.eject))
			self.templates[-1][0].body = 'eject'
			self.createMasterTemplate()
		
		async def eject(self, count=2):
			await self.logInfo("agent2B::eject start")
			for _ in range(count):
				await self.agent.runSecs(secs=0.6, speed=-30, brakeOnCompletion=True)
				await self.agent.sleep(0.2)
				self.agent.port.float()
				degs=10-self.agent.readRotation()
				await self.agent.runDegs(degs=degs, speed=40, brakeOnCompletion=True)
				self.agent.resetRotation()
				await self.agent.sleep(1)
				self.agent.port.float()
			msg = spade.message.Message()
			msg.to = agentnames.agent11
			msg.body = 'ready'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = agentnames.output
			msg.body = 'ready'
			await self.send(msg)
			await self.logInfo("agent2B::eject end")

	def __init__(self, *args, **kwargs):
		# Forward all arguments to super since we don't really use any ourselves.
		super().__init__(*args, **kwargs)
		self.add_behaviour(self.Behaviour_start())
		self.add_behaviour(self.Behaviour())
		self.agentname = "2B"

	

def createAgent2B():
	return MotorAgent2B(agentnames.agent2B, "agent2B")