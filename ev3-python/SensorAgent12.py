from SensorAgent import SensorAgent, valid_colors
from MyBehaviour import CyclicBehaviour
import spade
import time

class SensorAgent12(SensorAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates.append((spade.template.Template(), self.checkBrickDrop))
			self.templates[-1][0].body = 'next brick'
			self.createMasterTemplate()

		async def checkBrickDrop(self):
			print("checkbrickdrop started!")
			self.logInfo(f"checkBrickDrop started:\nvalid colors = {valid_colors}\ncolor={self.agent.port.colorSensorEV3()}")
			if self.agent.port.colorSensorEV3() in valid_colors:
				msg = spade.message.Message()
				msg.to = 'agent1A@192.168.1.8'
				msg.body = 'brick ready'
				await self.send(msg)
			else:
				self.logInfo(f"Expected brick in {valid_colors}. Actually scanned color = {self.agent.port.colorSensorEV3()}")
				msg = spade.message.Message()
				msg.to = 'output@192.168.1.8'
				msg.body = 'incorrect brick'
				await self.send(msg)
				time.sleep(1)
				msg = spade.message.Message()
				msg.to = 'agent11@192.168.1.8'
				msg.body = 'ready'
				await self.send(msg)

		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = '12'
		self.add_behaviour(self.Behaviour())

def createAgent12():
	return SensorAgent12("agent12@192.168.1.8", "agent12")