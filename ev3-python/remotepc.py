import ErrorAgent
import time
from spade import quit_spade
import asyncio

async def main():
	agents = [
		ErrorAgent.createErrorAgent()
	]
	time.sleep(5)

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
