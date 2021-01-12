from SensorAgent import SensorAgent, valid_colors, error_colors, any_brick, defaults
import time
from MyBehaviour import CyclicBehaviour
import spade
import agentnames

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
			await self.logInfo("agent14 updated brick color")
			self.agent.buckets = orders[index][:3]
			self.agent.build = orders[index][3]

		async def checkBrickBuildColor(self):
			await self.logInfo("agent14::checkBrickBuildColor start")
			msg = spade.message.Message()
			measuredColor = await self.agent.measureColor()
			if measuredColor == self.agent.build:
				msg.body = 'build'
				message = spade.message.Message()
				message.to = agentnames.agent1B
				message.body = 'build'
				await self.send(message)
			else:
				msg.body = 'sort'
				message = spade.message.Message()
				message.to = agentnames.agent14
				message.body = 'sort'
				await self.send(message)
			msg.to = agentnames.output
			await self.send(msg)
			await self.logInfo("agent14::checkBrickBuildColor end")

		async def checkValidColor(self):
			await self.logInfo("agent14::checkValidColor start")
			measuredColor = await self.agent.measureColor()
			if measuredColor in error_colors:
				await self.invalidColorNotify()
			else:
				await self.validColorNotify()
			await self.logInfo("agent14::checkValidColor end")
				
		async def invalidColorNotify(self):
			await self.logInfo("agent14::invalidcolornotify start")
			msg = spade.message.Message()
			msg.to = agentnames.output
			msg.body = 'color error'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = agentnames.agent14
			msg.body = 'color error'
			await self.send(msg)
			await self.logInfo("agent14::invalidcolornotify end")
		
		async def validColorNotify(self):
			await self.logInfo("agent14::validcolornotify start")
			msg = spade.message.Message()
			msg.to = agentnames.agent14
			msg.body = 'scan sort/build'
			await self.send(msg)
			await self.logInfo("agent14::validcolornotify start")

		async def waitValidColor(self):
			await self.logInfo("agent14::waitvalidcolor start")
			while (True):
				measuredColor = await self.agent.measureColor()
				if measuredColor in valid_colors:
					break
				await self.agent.sleep(0.5)
			await self.validColorNotify()
			await self.logInfo("agent14::waitvalidcolor end")

		async def sortGetBucketType(self):
			await self.logInfo("agent14::sortGetBucketType start")
			value = await self.agent.measureColor()
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
				await self.logError("Encountered sort color error")
				message = spade.message.Message()
				message.to = agentnames.output
				message.body = 'sort color error'
				await self.send(message)
				await self.agent.sleep(3) # Sleep so error message has time to appear
				# Not much point immediately replacing it with the menu
				message = spade.message.Message()
				message.to = agentnames.agent11
				message.body = 'ready'
				await self.send(message)
				message = spade.message.Message()
				message.to = agentnames.output
				message.body = 'ready'
				await self.send(message)
				return
			message = spade.message.Message()
			message.metadata = {"parameter": "sort"}
			message.thread = "1"
			message.to = agentnames.agent1B
			message.body = f"{value}"
			await self.send(message)
			await self.logInfo("agent14::sortGetbuckettype end")

		async def checkAnyBrickArrival(self):
			await self.logInfo("agent14::checkAnyBrickArrival start")
			measuredColor = await self.agent.measureColor()
			if measuredColor in any_brick:
				msg = spade.message.Message()
				msg.to = agentnames.agent1C
				msg.body = "brick arrived"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agent1B
				msg.body = "brick arrived"
				await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agent14
				msg.body = "check color"
				await self.send(msg)
			else:
				msg = spade.message.Message()
				msg.to = agentnames.agent13
				msg.body = 'proximity check'
				await self.send(msg)
			await self.logInfo("agent14::checkAnyBrickArrival end")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = '14'
		self.add_behaviour(self.Behaviour())
		self.buckets = defaults[:3]
		self.build = defaults[3]

def createAgent14():
	return SensorAgent14(agentnames.agent14, "agent14")