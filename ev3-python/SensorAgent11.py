from SensorAgent import SensorAgent
import spade
from MyBehaviour import CyclicBehaviour

class SensorAgent11(SensorAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates = []
			self.templates.append((spade.template.Template(), self.waitMenuTouch))
			self.templates[-1][0].body = 'ready'
			self.createMasterTemplate()
		
		async def waitMenuTouch(self):
			print("Waitmenutouch started")
			# see below, not implemented so far
			msg = spade.message.Message()
			msg.to = 'agent12@192.168.1.8'
			msg.body = 'next brick'
			await self.send(msg)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = '11'
		self.add_behaviour(self.Behaviour())

	# The EV3 brick has touch button sensors that are used in scratch to interact with the menu
	# The PiStorms version does not have these buttons.

	# This could be implemented with the touchscreen, but that implementation is a lot less trivial
	# Since this implementation doesn't really affect much, I've decided to leave it out. 

	# Since the system configurability (which bucket gets which color/build color)
	# Doesn't really impact the Multi-Agent system design,
	# I've decided not to implement this part of the scratch code. 

	# The sorting order can be changed by changing the defaults list in SensorAgent.py
	# The list contains [default_bucket1, default_bucket2, default_bucket3, default_build]
	# Which, per scratch code, is 2, 4, 6, 5


def createAgent11():
	return SensorAgent11("agent11@192.168.1.8", "agent11")