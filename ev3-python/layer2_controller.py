import MotorAgent2D
import MotorAgent2B
import MotorAgent2C
import asyncio
from main import main

if __name__ == "__main__":
	agentFunctions = [
		MotorAgent2B.createAgent2B,
		MotorAgent2C.createAgent2C,
		MotorAgent2D.createAgent2D
	]
	asyncio.run(main(agentFunctions))