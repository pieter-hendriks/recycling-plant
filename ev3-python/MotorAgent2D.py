from MotorAgent import MotorAgent
import time
from MyBehaviour import OneShotBehaviour, CyclicBehaviour
import spade 
import agentnames

class MotorAgent2D(MotorAgent):
	class Behaviour_start(OneShotBehaviour):
		async def run(self): # R_PRS
			await self.agent.sleep(10) # Wait for other agents to finish setup/clear prod line
			# 2C most importantly needs to clear the press surface!
			print("Agent2D run start")
			await self.logInfo("agent2D::run start")
			print("Agent2D info logged")
			self.agent.port.setSpeed(-10)
			await self.agent.sleep(0.1)
			await self.agent.runSecs(speed=-70, secs=1, brakeOnCompletion=True)
			await self.agent.sleep(0.1)
			self.agent.resetRotation()
			# Send messages signalling end of this routine
			msg = spade.message.Message()
			msg.to = agentnames.output
			msg.body = "ready"
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = agentnames.agent11
			msg.body = "ready"
			await self.send(msg)
			await self.logInfo("agent2D::run end")



	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.press))
			self.templates[-1][0].metadata = { "parameter": "press" }
			self.templates[-1][0].thread = "1"
			self.createMasterTemplate()
		
		async def press(self, count):
			await self.logInfo("agent2D::Press start")
			# We get message when agent1b is done rotating, but the brick might not
			# Have finished moving yet, so wait a bit
			# Then move and press down
			await self.agent.sleep(3)
			for _ in range(count):
				await self.agent.runSecs(secs=1, speed=50, brakeOnCompletion=False)
				self.agent.port.setSpeed(-8)
				await self.agent.sleep(0.1)
				degs = -50 - self.agent.readRotation()
				await self.agent.runDegs(degs=degs, speed=-20, brakeOnCompletion=True)
			degs = -20 - self.agent.readRotation()
			await self.agent.runDegs(degs=degs, speed=-20, brakeOnCompletion=True)
			await self.agent.sleep(0.2)
			self.agent.port.float()
			if count == 1:
				msg = spade.message.Message()
				msg.to = agentnames.output
				msg.body = 'ready'
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agent11
				msg.body = 'ready'
				await self.send(msg)
			elif count == 2:
				msg = spade.message.Message()
				msg.to = agentnames.output
				msg.body = 'eject'
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agent2B
				msg.body = 'eject'
				await self.send(msg)
			else:
				msg = spade.message.Message()
				msg.to = agentnames.agent2D
				msg.body = f"Count invalid value in press: {count}"
				await self.logError(msg)
			await self.logInfo("agent2D::Press end")

	def __init__(self, *args, **kwargs):
		# Forward all arguments to super since we don't really use any ourselves.
		super().__init__(*args, **kwargs)
		self.agentname = "2D"
		self.add_behaviour(self.Behaviour_start())
		self.add_behaviour(self.Behaviour())



def createAgent2D():
	return MotorAgent2D(agentnames.agent2D, "agent2D")