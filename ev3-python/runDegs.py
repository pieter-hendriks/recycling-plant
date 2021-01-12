import time

def runDegs(self, degs = 0, speed = 10, pollInterval = 0.2, brakeOnCompletion = False, holdOnCompletion = False):
		if not self.port or degs == 0 or speed == 0:
			return -2
		degs = abs(degs) # Degrees are always positive, direction is set by speed
		ret = 0
		self.port.setSpeed(speed)
		while (True): 
			time.sleep(pollInterval)
			oldRotation = self.port.pos()
			newRotation = self.port.pos()
			if (oldRotation == newRotation):
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
		return ret
