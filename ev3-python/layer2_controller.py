import MotorAgent2D
import MotorAgent2B
import MotorAgent2C
import OutputAgent
import asyncio
from spade import quit_spade
import time

async def main():
	agents = [
		MotorAgent2B.createAgent2B(),
		MotorAgent2C.createAgent2C(),
		MotorAgent2D.createAgent2D(),
		OutputAgent.createOutputAgent()
	]

	for agent in agents:
		agent.start()

	try:
		while(True):
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