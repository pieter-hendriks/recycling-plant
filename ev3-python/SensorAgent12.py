from SensorAgent import SensorAgent, valid_colors
from MyBehaviour import CyclicBehaviour
import spade
import time
import agentnames

class SensorAgent12(SensorAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates.append((spade.template.Template(), self.checkBrickDrop))
			self.templates[-1][0].body = 'next brick'
			self.createMasterTemplate()

		async def checkBrickDrop(self):
			await self.logInfo("agent12::checkBrickDrop start")
			scanColor = await self.agent.measureColor()
			
			await self.logInfo(f"agent12::checkBrickDrop:\nvalid colors = {valid_colors}\ncolor={scanColor}")
			if scanColor in valid_colors:
				msg = spade.message.Message()
				msg.to = agentnames.agent1A
				msg.body = 'brick ready'
				await self.send(msg)
			else:
				await self.logInfo(f"Expected brick in {valid_colors}. Actually scanned color = {scanColor}")
				msg = spade.message.Message()
				msg.to = agentnames.output
				msg.body = 'incorrect brick'
				await self.send(msg)
				await self.agent.sleep(1)
				msg = spade.message.Message()
				msg.to = agentnames.agent11
				msg.body = 'ready'
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.output
				msg.body = 'ready'
				await self.send(msg)
			await self.logInfo("agent12::checkBrickDrop end")

		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = '12'
		self.add_behaviour(self.Behaviour())

def createAgent12():
	return SensorAgent12(agentnames.agent12, "agent12")