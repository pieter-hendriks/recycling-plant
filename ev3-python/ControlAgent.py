import spade
import agentnames

class ControlAgent(spade.agent.Agent):
	class InputBehaviour(spade.behaviour.CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

		async def run(self):
			userInput = input("Please enter control command:\n")
			userInput = userInput.split(' ')
			msg = spade.message.Message()
			if userInput[0] == 'msg':
				# Send message to agent, with given body (metadata optional)
				assert len(userInput) == 4 or len(userInput) == 3
				msg.to = eval(f'agentnames.{userInput[1]}')
				if userInput[2][0] == "'":
					txt = ' '.join(userInput[2:])
					txt = txt.split("'")
					userInput = [userInput[0], userInput[1], txt[1]] + "'".join(txt).split(' ')
				elif userInput[2][0] == '"':
					txt = ' '.join(userInput[2:])
					txt = txt.split('"')

				msg.body = userInput[2]
				msg.metadata = eval(userInput[3])
			elif userInput[0] == 'stop':
				# Stop all action on the recycling line, makes all motors .float()
				assert len(userInput) == 1
				for agent in agentnames.agentNames[:-1]:
					msg = spade.message.Message()
					msg.to = agent
					msg.body = 'stop'
					await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agentNames[-1]
				msg.body = 'stop'
			elif userInput[0] == 'build':
				# Sets the build color
				assert len(userInput) == 2
				msg.to = agentnames.agent14
				if userInput[1] not in [0, 1, 2, 3]:
					print(f"{userInput[1]} is an invalid index for build color. Must be in [0, 1, 2, 3].")
					print("Leaving the value unchanged.")
					return
				msg.body = f'run updateBrickOrder {userInput[1]}'
			elif userInput[0] == 'set':
				# Force a certain value onto a sensor
				assert len(userInput) == 3
				msg.to = eval(f'agentnames.{userInput[1]}')
				msg.body = f"set {userInput[2]}"
			elif userInput[0] == 'sethold':
				# Force (and hold) a certain value onto a sensor
				assert len(userInput) == 3
				msg.to = eval(f'agentnames.{userInput[1]}')
				msg.body = f"sethold {userInput[2]}"
			elif userInput[0] == 'run':
				msg.to = eval(f'agentnames.{userInput[1]}')
				msg.body = f'run {" ".join(userInput[2:])}'
			elif userInput[0] == 'getinfo':
				assert len(userInput) == 1
				for agent in agentnames.agentNames[:-1]:
					msg = spade.message.Message()
					msg.to = agent
					msg.body = 'getinfo'
					await self.send(msg)
				msg = spade.message.Message()
				msg.to = agentnames.agentNames[-1]
				msg.body = 'getinfo'
			else:
				print(f"Unfortunately, no behaviour is programmed for the command '{userInput}'.")
				print("Please ensure you're entering a valid command.")
			print("outputting the following control message: ")
			print(msg.body)
			msg.sender = agentnames.control
			await self.send(msg)
			
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	async def setup(self):
		self.add_behaviour(self.InputBehaviour())

def createControlAgent():
	return ControlAgent(agentnames.control, "control")

	