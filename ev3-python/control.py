from ControlAgent import createControlAgent
import asyncio
import time

async def main():
	agent = createControlAgent()
	ret = agent.start()
	if asyncio.iscoroutine(ret):
		await ret
	else:
		ret.result()
	try:
		while (True):
			time.sleep(2)
	except KeyboardInterrupt:
		pass
	finally:
		ret = agent.stop()
		if asyncio.iscoroutine(ret):
			await ret
		else:
			ret.result()

if __name__ == "__main__":
	asyncio.run(main())