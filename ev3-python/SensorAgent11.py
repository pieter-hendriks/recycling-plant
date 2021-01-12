from SensorAgent import SensorAgent
import spade
from MyBehaviour import CyclicBehaviour
from PiStorms import PiStormsSensor
import time
import agentnames

class SensorAgent11(SensorAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.waitMenuTouch))
			self.templates[-1][0].body = 'ready'
			self.createMasterTemplate()

		async def waitMenuTouch(self):
			await self.logInfo("agent11::waitmenutouch start")
			while (True):
				touched = await self.agent.measureTouch(0.5, 5)
				if touched:
					break
				await self.agent.sleep(1)
			msg = spade.message.Message()
			msg.to = agentnames.agent12
			msg.body = 'next brick'
			await self.send(msg)
			await self.logInfo("agent11::waitmenutouch end")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = '11'
		self.add_behaviour(self.Behaviour())


def createAgent11():
	return SensorAgent11(agentnames.agent11, "agent11")