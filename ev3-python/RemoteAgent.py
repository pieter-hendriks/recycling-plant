import spade

class RemoteAgent(spade.agent.Agent):
	class LogBehaviour(spade.behaviour.CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

		async def run(self):
			msg = await self.receive(timeout = 5)
			if msg:
				print(f"Error encountered by an agent:\n{msg.body}")
				print("Remote agent waiting for input: ")
			else:
				pass # No errors logged
	
	class InputBehaviour(spade.behaviour.CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

		async def run(self):
			userInput = input("Remote agent waiting for input: ")
			if userInput == 'reset':
				pass
			elif userInput == 'stop':
				pass
			elif userInput == 'build1':
				pass
			elif userInput == 'build2':
				pass
			elif userInput == 'build3':
				pass
			elif userInput == 'build4':
				pass
			else:
				print(f"Unfortunately, no behaviour is programmed for the command '{userInput}'.")
				print("Please ensure you're entering a valid command.")
			
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	async def setup(self):
		self.add_behaviour(self.LogBehaviour())
		self.add_behaviour(self.InputBehaviour())

def createRemoteAgent():
	return RemoteAgent("error@192.168.1.8", "error")