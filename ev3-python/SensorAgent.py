from MyAgent import MyAgent
from PiStorms import PiStorms, PiStormsSensor
from PiStormsCom import PSSensor
from collections import Counter
import time

def mode(l):
	return Counter(l).most_common(1)[0][0]

COLOR_NONE = PiStormsSensor.PS_SENSOR_COLOR_NONE
COLOR_BLACK = PiStormsSensor.PS_SENSOR_COLOR_BLACK
COLOR_BLUE = PiStormsSensor.PS_SENSOR_COLOR_BLUE
COLOR_GREEN = PiStormsSensor.PS_SENSOR_COLOR_GREEN
COLOR_YELLOW = PiStormsSensor.PS_SENSOR_COLOR_YELLOW
COLOR_RED = PiStormsSensor.PS_SENSOR_COLOR_RED
COLOR_WHITE = PiStormsSensor.PS_SENSOR_COLOR_WHITE
COLOR_BROWN = PiStormsSensor.PS_SENSOR_COLOR_BROWN

valid_colors = [COLOR_BLUE, COLOR_YELLOW, COLOR_RED, COLOR_WHITE]
error_colors = [COLOR_BLACK, COLOR_BROWN]
any_brick = [COLOR_BLACK, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_RED, COLOR_WHITE, COLOR_BROWN]
# Bucket1, bucket2, bucket3, build
defaults = [2, 4, 6, 5]

class SensorAgent(MyAgent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	async def setup(self):
		await super().setup()
		print(f"Hi! I'm SensorAgent {self.agentname}, with id {self.jid}.")
		self.psm :PiStorms = PiStorms()
		assert self.agentname is not None
		if self.agentname[1] == '1':
			self.port = self.psm.BAS1
			self.port.pssensor.setType(PSSensor.PS_SENSOR_TYPE_EV3_SWITCH)
			self.measureFn = self.port.isTouchedEV3
		elif self.agentname[1] == '2':
			self.port = self.psm.BAS2
			self.port.pssensor.setType(PSSensor.PS_SENSOR_TYPE_EV3)
			self.measureFn = self.port.colorSensorEV3
		elif self.agentname[1] == '3':
			self.port = self.psm.BBS1
			self.port.pssensor.setType(PSSensor.PS_SENSOR_TYPE_EV3)
			self.measureFn = self.port.distanceUSEV3
		elif self.agentname[1] == '4':
			self.port = self.psm.BBS2
			self.port.pssensor.setType(PSSensor.PS_SENSOR_TYPE_EV3)
			self.measureFn = self.port.colorSensorEV3

	def getInfo(self):
				return (f"Sensor {self.name} is currently measuring {self.__measure()}")

	async def __measure(self, measureFn = None, timePeriod = 1, measurementCount = 5, aggrFn = lambda x: sum(x) / len(x)):
		if measureFn == None:
			measureFn = self.measureFn
		if self.nextValue is not None:
			if self.holdConfiguredValue:
				return self.nextValue
			v = self.nextValue
			self.nextValue = None
			return v
		measureFn() # Do one measurement, pre-emptively
		# When a color sensor is in the wrong mode, at first, it might return a wrong value
		# So we ensure it's correctly set before we start recording results 
		# (Other sensors presumably have similar problems, but those aren't visually indicated)
		# Color sensor emits different color light when set incorrectly, others don't emit anything.
		measurements = []
		interval = timePeriod / (1.0 * measurementCount)
		for _ in range(measurementCount):
			measurements.append(measureFn())
			await self.sleep(interval)
		print(f"{self.jid} measurements: {measurements}")
		return aggrFn(measurements)

	async def measureColor(self, timePeriod = 1, measurementCount = 10):
		assert self.agentname == '12' or self.agentname == '14'
		return await self.__measure(self.measureFn, timePeriod, measurementCount, mode)

	async def measureTouch(self, timePeriod = 0.5, measurementCount = 5):
		assert self.agentname == '11'
		return await self.__measure(self.measureFn, timePeriod, measurementCount, mode)

	async def measureDistance(self, timePeriod = 1, measurementCount = 10):
		assert self.agentname == '13'
		return await self.__measure(self.measureFn, timePeriod, measurementCount, lambda x: sum(x) / float(len(x)))