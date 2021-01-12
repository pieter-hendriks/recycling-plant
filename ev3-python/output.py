import RemoteAgent
import ControlAgent
import asyncio
from main import main

	
if __name__ == "__main__":
	agentFunctions = [
		RemoteAgent.createRemoteAgent
	]
	asyncio.run(main(agentFunctions))