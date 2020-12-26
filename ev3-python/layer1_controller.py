import MotorAgent1A
import MotorAgent1B
import MotorAgent1C
import SensorAgent11
import SensorAgent12
import SensorAgent13
import SensorAgent14
import OutputAgent
from spade import quit_spade
import time
import asyncio
async def main():
	agents = [
		MotorAgent1A.createAgent1A(),
		MotorAgent1B.createAgent1B(),
		MotorAgent1C.createAgent1C(),
		SensorAgent11.createAgent11(),
		SensorAgent12.createAgent12(),
		SensorAgent13.createAgent13(),
		SensorAgent14.createAgent14(),
		OutputAgent.createOutputAgent()
	]
	for agent in agents:
		agent.start()


	try:
		while (True):
			time.sleep(5)
	except KeyboardInterrupt:
		pass
	finally:
		for agent in agents:
			agent.stop()
		quit_spade()
	exit(0)


if __name__ == "__main__":
	asyncio.run(main())