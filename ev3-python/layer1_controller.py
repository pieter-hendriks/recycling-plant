import MotorAgent1A
import MotorAgent1B
import MotorAgent1C
import SensorAgent11
import SensorAgent12
import SensorAgent13
import SensorAgent14
import OutputAgent
import asyncio
from main import main

if __name__ == "__main__":
	agentFunctions = [
		MotorAgent1A.createAgent1A,
		MotorAgent1B.createAgent1B,
		MotorAgent1C.createAgent1C,
		SensorAgent11.createAgent11,
		SensorAgent12.createAgent12,
		SensorAgent13.createAgent13,
		SensorAgent14.createAgent14,
		OutputAgent.createOutputAgent
	]
	asyncio.run(main(agentFunctions))