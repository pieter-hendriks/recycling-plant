from MyAgent import MyAgent
from PiStorms import PiStorms, PiStormsMotor
from PiStormsCom import PSMotor
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import asyncio
import time
import math
class MotorAgent(MyAgent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Bandaid fix because system doesn't expose resetRotation
		# Though I've manually put it in there, hope I didn't break anythign!!
		self.speed = 0
		self.active = False

	def getInfo(self):
		return (
			f"Motor {self.name} is currently rotated {self.readRotation()} degrees.\n"
			f"It is not currently active." if not self.active else f"It is currently rotating at speed {self.speed}."
		)
		
	def __getPort(self):
		assert self.agentname is not None
		if self.agentname[1] == "A":
			return self.psm.BAM1
		elif self.agentname[1] == "B":
			return self.psm.BAM2
		elif self.agentname[1] == "C":
			return self.psm.BBM1
		elif self.agentname[1] == "D":
			return self.psm.BBM2

	def readRotation(self):
		if self.nextValue is not None:
			if self.holdConfiguredValue:
				return self.nextValue
			v = self.nextValue
			self.nextValue = None
			return v
		positions = []
		for _ in range(11):
			positions.append(self.port.pos())
		return sorted(positions)[math.floor(len(positions) / 2)]

	def resetRotation(self):
		self.port.resPos()

	async def setup(self):
		await super().setup()
		print(f"Hi! I'm MotorAgent {self.agentname}, with id {self.jid}.")
		self.psm :PiStorms = PiStorms()
		self.port :PiStormsMotor = self.__getPort()
	
	# Synchronous, approximate versions of the implementation in PiStorms API
	# runDegs function appears to be broken, so we'll replace those with our own version
	async def runDegs(self, degs = 0, speed = 10, pollInterval = 0.15, brakeOnCompletion = False, holdOnCompletion = False):
		if not self.port or degs == 0 or speed == 0:
			return -2
		print(f"{self.jid} running {degs} degrees at speed {speed}")
		degs = abs(degs) # Degrees are always positive, direction is set by speed
		if (degs > 2500):
			degs = 2500
			# Hard-coded maximum rotation to avoid stupidly long runtimes.
		print(f"{self.jid} running (after correction) {degs} degrees at speed {speed}")
		ret = 0
		self.resetRotation()
		self.port.setSpeed(speed)
		self.active = True
		self.speed = speed
		oldRotation = self.readRotation()
		newRotation = None
		while (True): 
			await self.sleep(pollInterval)
			previousRotation = newRotation
			newRotation = self.readRotation()
			print(f"{self.jid} runDegs iteration: currentRotation = {newRotation - oldRotation}")
			if (previousRotation == newRotation):
				self.port.float()
				ret = -1
				break
			elif abs(newRotation - oldRotation) >= degs:
				ret = 0
				break
		if brakeOnCompletion:
			self.port.brake()
		if holdOnCompletion:
			self.port.hold()
		if not brakeOnCompletion and not holdOnCompletion:
			self.port.float()
		self.active = False
		self.speed = 0
		return ret

	# Synchronous runSecs version also makes more sense than asynchronous one - we just want to 
	# Run the motor for the specified amount of time and wait for it to finish, generally.
	# Agent won't want to do anything else until its task has been completed.
	async def runSecs(self, secs = 0, speed = 10, brakeOnCompletion=False, holdOnCompletion=False):
		if not self.port or secs == 0 or speed == 0:
			return -2
		self.port.setSpeed(speed)
		self.active = True
		self.speed = speed
		await self.sleep(secs)
		if brakeOnCompletion:
			self.port.brake()
		if holdOnCompletion:
			self.port.hold()
		if not brakeOnCompletion and not holdOnCompletion:
			self.port.float()
		self.active = False
		self.speed = 0
		return 0
	
	async def stop(self):
		print(f"{self.jid} stopping: port.float() called!")
		self.port.float()
		self.active = False
		self.speed = 0
		task = super().stop()
		if asyncio.iscoroutine(task):
			await task
		else:
			task.result()
		
