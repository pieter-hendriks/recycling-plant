from SensorAgent import SensorAgent
import time
from MyBehaviour import CyclicBehaviour
import spade

class SensorAgent13(SensorAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates.append((spade.template.Template(), self.checkBarrier))
			self.templates[-1][0].body = 'proximity check'
			self.templates.append((spade.template.Template(), self.checkBarrierStop))
			self.templates[-1][0].body = 'proximity alert'
			self.createMasterTemplate()

		async def checkBarrier(self):
			if self.agent.port.distanceUSEV3() < 20:
				msg = spade.message.Message()
				msg.to = "output@192.168.1.8"
				msg.body = "proximity alert"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = "agent13@192.168.1.8"
				msg.body = "proximity alert"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = "agent1B@192.168.1.8"
				msg.body = "proximity alert"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = "agent1C@192.168.1.8"
				msg.body = "proximity alert"
				await self.send(msg)
			else: 
				msg = spade.message.Message()
				msg.body = 'maybe stuck'
				msg.to = "agent1B@192.168.1.8"
				await self.send(msg)
				# Broadcast all-clear
				pass
			
		async def checkBarrierStop(self):
			while (self.agent.port.distanceUSEV3() <= 30):
				time.sleep(0.2)
			msg = spade.message.Message()
			msg.body = 'area clear'
			msg.to = 'agent1B@192.168.1.8'
			await self.send(msg)
			msg = spade.message.Message()
			msg.body = 'area clear'
			msg.to = 'agent1C@192.168.1.8'
			await self.send(msg)
			msg = spade.message.Message()
			msg.body = 'area clear'
			msg.to = 'output@192.168.1.8'
			await self.send(msg)
			time.sleep(1)
			msg = spade.message.Message()
			msg.body = 'maybe stuck'
			msg.to = "agent1B@192.168.1.8"
			await self.send(msg)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = '13'
		self.add_behaviour(self.Behaviour())



def createAgent13():
	return SensorAgent13("agent13@192.168.1.8", "agent13")