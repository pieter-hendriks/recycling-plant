import spade

class CyclicBehaviour(spade.behaviour.CyclicBehaviour):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.templates = []
	
	def createMasterTemplate(self):
		master = self.templates[0][0]
		for i in range(1, len(self.templates)):
			master = spade.template.ORTemplate(master, self.templates[i][0])
		self.set_template(master)
	async def on_start(self):
		self.templates.append((None, self.logError))
	
	async def run(self):
		msg = await self.receive(timeout = 5)
		if msg:
			print(f"Agent {self.agent.jid} has received the following message:\n{msg}")
			for t, fn in self.templates:
				if t is None:
					await fn(msg)
					break # THough this one should always be the last one!
				elif t.match(msg):
					if "parameter" in t.metadata:
						await fn(int(msg.body))
						break
					else:
						await fn()
						break
	
	async def logError(self, msg):
		message = spade.message.Message()
		message.to = "error@192.168.1.8"
		message.thread = "0"
		message.body = f"{self.agent.jid} encountered an error, unprocessed message:\n{msg.sender}\n{msg.body}"
		await self.send(message)
	
	async def logInfo(self, msg):
		message = spade.message.Message()
		message.to = "error@192.168.1.8"
		message.thread = "2"
		message.body = f"Information from {self.agent.jid}:\n{msg}"
		await self.send(message)
		
class OneShotBehaviour(spade.behaviour.OneShotBehaviour):
	async def logError(self, msg):
		message = spade.message.Message()
		message.to = "error@192.168.1.8"
		message.thread = "0"
		message.body = f"{self.agent.jid} encountered an error, unprocessed message:\n{msg.sender}\n{msg.body}"
		await self.send(message)
	
	async def logInfo(self, msg):
		message = spade.message.Message()
		message.to = "error@192.168.1.8"
		message.thread = "2"
		message.body = f"Information from {self.agent.jid}:\n{msg}"
		await self.send(message)

# Must be a way to avoid the code duplication, but no free functions makes it a little hard.
# JUst duplicating is simple.