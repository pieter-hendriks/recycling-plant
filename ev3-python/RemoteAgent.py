import spade
import agentnames
class RemoteAgent(spade.agent.Agent):
	class LogBehaviour(spade.behaviour.CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
		async def run(self):
			msg = await self.receive(timeout = 5)
			if msg:
				handled = False
				if msg.metadata and "type" in msg.metadata:
					if msg.metadata["type"] == "error":
						print(f"Error encountered by {msg.sender}:\n{msg.body}")
						handled = True
					elif msg.metadata["type"] == "info":
						print(f"Information from {msg.sender}:\n{msg.body}")
						handled = True
					elif msg.metadata["type"] == "unprocessed":
						print(f"Unprocessed message encountered by {msg.sender}:\n{msg.body}")
						handled = True
				if not handled:
					print(f"Message received but not handled:\n{msg}")
			else:
				pass # No errors logged
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	async def setup(self):
		self.add_behaviour(self.LogBehaviour())
		print("Remote agent setup complete")

def createRemoteAgent():
	return RemoteAgent(agentnames.error, "error")