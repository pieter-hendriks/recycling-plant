from MyAgent import MyAgent
from PiStorms import PiStorms, PiStormsSensor

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
	def __getPort(self):
		assert self.agentname is not None
		if self.agentname[1] == '1':
			return self.psm.BAS1
		elif self.agentname[1] == '2':
			return self.psm.BAS2
		elif self.agentname[1] == '3':
			return self.psm.BBS1
		elif self.agentname[1] == '4':
			return self.psm.BBS2

	async def setup(self):
		await super().setup()
		print(f"Hi! I'm SensorAgent {self.agentname}, with id {self.jid}.")
		self.psm :PiStorms = PiStorms()
		self.port : PiStormsSensor = self.__getPort()
