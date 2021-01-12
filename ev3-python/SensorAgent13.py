from SensorAgent import SensorAgent
import time
from MyBehaviour import CyclicBehaviour
import spade
from PiStorms import PiStormsSensor
import agentnames
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
			await self.logInfo("agent13::checkBarrier start")
			distance = await self.agent.measureDistance() 
			if distance < 200: # 20cm
				await self.logInfo("agent13::checkBarrier proximity alert")
				msg = spade.message.Message()
				msg.to = agentnames.output
				msg.body = "proximity alert"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agent13
				msg.body = "proximity alert"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agent1B
				msg.body = "proximity alert"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agent1C
				msg.body = "proximity alert"
				await self.send(msg)
			else: 
				await self.logInfo("agent13::checkBarrier area clear")
				msg = spade.message.Message()
				msg.body = 'maybe stuck'
				msg.to = agentnames.agent1B
				await self.send(msg)
				# Broadcast all-clear
			await self.logInfo("agent13::checkBarrier end")
			
		async def checkBarrierStop(self):
			await self.logInfo("agent13::checkBarrierStop start")
			while (True):
				distance = await self.agent.measureDistance()
				if distance > 300: 
					break
				await self.agent.sleep(2)
			await self.logInfo("agent13::checkBarrierStop area clear")
			msg = spade.message.Message()
			msg.body = 'area clear'
			msg.to = agentnames.agent1B
			await self.send(msg)
			msg = spade.message.Message()
			msg.body = 'area clear'
			msg.to = agentnames.agent1C
			await self.send(msg)
			msg = spade.message.Message()
			msg.body = 'area clear'
			msg.to = agentnames.output
			await self.send(msg)
			await self.agent.sleep(1)
			msg = spade.message.Message()
			msg.body = 'maybe stuck'
			msg.to = agentnames.agent1B
			await self.send(msg)
			await self.logInfo("agent13::checkBarrierStop end")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = '13'
		self.add_behaviour(self.Behaviour())



def createAgent13():
	return SensorAgent13(agentnames.agent13, "agent13")