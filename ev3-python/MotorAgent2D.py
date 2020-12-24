from MotorAgent import MotorAgent
import time
from MyBehaviour import OneShotBehaviour, CyclicBehaviour
import spade 
class MotorAgent2D(MotorAgent):
	class Behaviour_start(OneShotBehaviour):
		async def run(self): # R_PRS
			self.agent.port.runSecs(speed=-2.5, secs=0.3, brakeOnCompletion=True)
			self.agent.port.setSpeed(8)
			time.sleep(0.3)
			#self.agent.port.waitUntilNotBusy()
			self.agent.port.brake()
			# God I hope this works
			#self.agent.port.waitUntilNotBusy()
			self.agent.resetRotation()
			self.agent.port.float()
			# Send messages signalling end of this routine
			msg = spade.message.Message()
			msg.to = "output@192.168.1.8"
			msg.body = "ready"
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = "agent11@192.168.1.8"
			msg.body = "ready"
			await self.send(msg)



	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.press))
			self.templates[-1][0].metadata = { "parameter": "press" }
			self.templates[-1][0].thread = "1"
			self.createMasterTemplate()
		
		async def press(self, count):
			for _ in range(count):
				self.agent.port.runSecs(secs=1, speed=-50, brakeOnCompletion=False)
				degs = -50 - self.agent.readRotation()
				self.agent.port.runDegs(degs=degs, speed=20, brakeOnCompletion=True)
			degs = -20 - self.agent.readRotation()
			self.agent.port.runDegs(degs=degs, speed=20, brakeOnCompletion=True)
			time.sleep(0.2)
			self.agent.port.hold()
			if count == 1:
				msg = spade.message.Message()
				msg.to = 'output@192.168.1.8'
				msg.body = 'next brick'
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = 'agent11@192.168.1.8'
				msg.body = 'next brick'
				await self.send(msg)
			elif count == 2:
				msg = spade.message.Message()
				msg.to = 'output@192.168.1.8'
				msg.body = 'eject'
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = 'agent2B@192.168.1.8'
				msg.body = 'eject'
				await self.send(msg)
			else:
				msg = spade.message.Message()
				msg.to = "agent2D@192.168.1.8"
				msg.body = f"Count invalid value in press: {count}"
				self.logError(msg)

	def __init__(self, *args, **kwargs):
		# Forward all arguments to super since we don't really use any ourselves.
		super().__init__(*args, **kwargs)
		self.agentname = "2D"
		self.add_behaviour(self.Behaviour_start())
		self.add_behaviour(self.Behaviour())



def createAgent2D():
	return MotorAgent2D("agent2D@192.168.1.8", "agent2D")