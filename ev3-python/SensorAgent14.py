from SensorAgent import SensorAgent, valid_colors, error_colors, any_brick, defaults
import time
from MyBehaviour import CyclicBehaviour
import spade

orders = []
for i in range(4):
	orders.append([defaults[(i + j) % 4] for j in range(len(defaults))])


class SensorAgent14(SensorAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates.append((spade.template.Template(), self.checkValidColor))
			self.templates[-1][0].body = 'check color'
			self.templates.append((spade.template.Template(), self.waitValidColor))
			self.templates[-1][0].body = 'color error'
			self.templates.append((spade.template.Template(), self.sortGetBucketType))
			self.templates[-1][0].body = 'sort'
			self.templates.append((spade.template.Template(), self.checkAnyBrickArrival))
			self.templates[-1][0].body = 'no stuck brick'
			self.templates.append((spade.template.Template(), self.checkBrickBuildColor))
			self.templates[-1][0].body = 'scan sort/build'
			self.templates.append((spade.template.Template(), self.updateBrickOrder))
			self.templates[-1][0].metadata = {"parameter": "order"}
			self.templates[-1][0].thread = "1"
			self.createMasterTemplate()

		async def updateBrickOrder(self, index):
			self.agent.buckets = orders[index][:3]
			self.agent.build = orders[index][3]

		async def checkBrickBuildColor(self):
			msg = spade.message.Message()
			msg.to = 'output@192.168.1.8'
			if self.agent.port.colorSensorEV3() == self.agent.build:
				msg.body = 'build'
				message = spade.message.Message()
				message.to = 'agent1B@192.168.1.8'
				message.body = 'build'
				await self.send(message)
			else:
				msg.body = 'sort'
				message = spade.message.Message()
				message.to = 'agent14@192.168.1.8'
				message.body = 'sort'
				await self.send(message)
			await self.send(msg)

		async def checkValidColor(self):
			if self.agent.port.colorSensorEV3() in error_colors:
				self.invalidColorNotify()
			else:
				self.validColorNotify()
				
		async def invalidColorNotify(self):
			msg = spade.message.Message()
			msg.to = 'output@192.168.1.8'
			msg.body = 'color error'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = 'agent14@192.168.1.8'
			msg.body = 'color error'
			await self.send(msg)
		async def validColorNotify(self):
			msg = spade.message.Message()
			msg.to = 'agent14@192.168.1.8'
			msg.body = 'scan sort/build'
			await self.send(msg)

		async def waitValidColor(self):
			while self.agent.port.colorSensorEV3() not in valid_colors:
				time.sleep(0.2)
			self.validColorNotify()

		async def sortGetBucketType(self):
			value = self.agent.port.colorSensorEV3()
			if value == self.agent.buckets[0]:
				value = 0
				pass # Broadcast sort bucket1
			elif value == self.agent.buckets[1]:
				value = 1
				pass # Broadcast sort bucket2
			elif value == self.agent.buckets[2]:
				value = 2
				pass # Broadcast sort bucket3
			else:
				message = spade.message.Message()
				message.to = 'output@192.168.1.8'
				message.body = 'sort color error'
				await self.send(message)
				time.sleep(3) # Sleep so error message has time to appear
				# Not much point immediately replacing it with the menu
				message = spade.message.Message()
				message.to = 'agent11@192.168.1.8'
				message.body = 'next brick'
				await self.send(message)
				message = spade.message.Message()
				message.to = 'output@192.168.1.8'
				message.body = 'next brick'
				await self.send(message)
				return
			message = spade.message.Message()
			message.metadata = {"parameter": "sort"}
			message.thread = "1"
			message.to = "agent1B@192.168.1.8"
			message.body = str(value)
			await self.send(message)

		async def checkAnyBrickArrival(self):
			if self.agent.port.colorSensorEV3() in any_brick:
				pass # Broadcast arrival
				msg = spade.message.Message()
				msg.to = "agent1C@192.168.1.8"
				msg.body = "brick arrived"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = "agent1B@192.168.1.8"
				msg.body = "brick arrived"
				await self.send(msg)
				time.sleep(0.2)
				msg = spade.message.Message()
				msg.to = "agent14@192.168.1.8"
				msg.body = "check color"
				await self.send(msg)
			else:
				msg = spade.message.Message()
				msg.to = "agent13@192.168.1.8"
				msg.body = 'proximity check'
				await self.send(msg)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = '14'
		self.add_behaviour(self.Behaviour())
		self.buckets = defaults[:3]
		self.build = defaults[3]

def createAgent14():
	return SensorAgent14("agent14@192.168.1.8", "agent14")