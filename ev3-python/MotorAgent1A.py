from MotorAgent import MotorAgent
import time
import spade
from MyBehaviour import OneShotBehaviour, CyclicBehaviour
import agentnames

class MotorAgent1A(MotorAgent):
	class Behaviour_start(OneShotBehaviour):
		async def run(self): # R_DRP
			self.agent.port.setSpeed(-8)
			await self.agent.sleep(0.1)
			await self.logInfo("agent1A::run start: Rotate to blocking spot, bottom orientation")
			await self.agent.runDegs(degs=360, speed=-10, brakeOnCompletion=True)
			# Do one rotation, should block on blocking spot and rest of the calls should work fine. 
			# self.agent.port.setSpeed(50)
			await self.logInfo("agent1A::run progress: Rotate back up a bit, ensure we're ready to push up the starting block")
			await self.agent.runDegs(degs=135, speed=20, brakeOnCompletion=True)
			await self.agent.sleep(0.1)
			self.agent.resetRotation()
			await self.logInfo("agent1A::run end")

	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates.append((spade.template.Template(), self.drop))
			self.templates[-1][0].body = "brick ready"
			self.createMasterTemplate()

		async def drop(self):
			await self.logInfo("agent1A::drop start")
			degs = 90 + self.agent.readRotation()
			if abs(degs) > 200:
				degs = 90 # Bandaid fix because it goes nuts sometimes
			await self.logInfo(f"agent1A motor running for 90 degrees, at speed 20")
			await self.agent.runDegs(degs=degs, speed=20, brakeOnCompletion=True)
			await self.logInfo(f"agent1A motor running for -90 degrees, at speed -20")
			await self.agent.runDegs(degs=-90, speed=-20, brakeOnCompletion=True)
			self.agent.resetRotation()
			self.agent.port.float()
			
			await self.logInfo("Agent1A notifying everyone for brick drop")
			# Send to everyone in Shred()
			msg = spade.message.Message()
			msg.to = agentnames.output
			msg.body = 'brick dropped'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = agentnames.agent1B
			msg.body = 'brick dropped'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = agentnames.agent1C
			msg.body = 'brick dropped'
			await self.send(msg)
			await self.logInfo("Agent1A notifying 13 for proximity check")
			# And continue onwards in the loop. 
			# Barrier might pause shred, but will resume it afterwards. 
			msg = spade.message.Message()
			msg.to = agentnames.agent13
			msg.body = 'proximity check'
			await self.send(msg)
			await self.logInfo("agent1A::drop end")

		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = "1A"
		self.add_behaviour(self.Behaviour_start())
		self.add_behaviour(self.Behaviour())

 
def createAgent1A():
	agent = MotorAgent1A(agentnames.agent1A, "agent1A")
	return agent
