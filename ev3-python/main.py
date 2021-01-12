import multiprocessing as mp
import time
import signal
import sys
import asyncio

def sigterm_handler(_signo, _stack_frame):
	sys.exit(0)

async def startFn(agentfn):
	signal.signal(signal.SIGTERM, sigterm_handler)
	try:
		agent = agentfn()
		ret = agent.start()
		if asyncio.iscoroutine(ret):
			await ret
		else:
			ret.result()
		while (True):
			time.sleep(60)
	finally:
		print("Endless loop end. Stopping agent.")
		ret = agent.stop()
		if asyncio.iscoroutine(ret):
			await ret
		else:
			ret.result()

async def child_main():
	try: 
		while (True):
			time.sleep(2)
	except KeyboardInterrupt:
		sys.exit(0)

def syncStartFn(agentfn):
	asyncio.run(startFn(agentfn))

async def main(agentFunctions):
	processes = []
	for agentFn in agentFunctions:
		processes.append(mp.Process(target=syncStartFn, args=(agentFn,)))
		processes[-1].start()

	try:
		while (True):
			time.sleep(2)
	except KeyboardInterrupt:
		for process in processes:
			process.terminate()
		for process in processes:
			process.join()

	
