import spade
import agentnames
import inspect

class ControlBehaviour(spade.behaviour.CyclicBehaviour):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		template = spade.template.Template()
		template.sender = agentnames.control
		self.set_template(template)

	# We don't use these on control behaviour, but simplifies message handling
	def enableMessages(self):
		pass
	def disableMessages(self):
		pass

	async def run(self):
		print(f"{self.agent.jid} control behaviour running!")
		msg = await self.receive(timeout = 30)
		if msg:
			body = msg.body.split(' ')
			if body[0] == 'run':
				if hasattr(self.agent, body[1]) and callable(getattr(self.agent, body[1])):
					fn = lambda s: eval(f"s.agent.{body[1]}({', '.join(body[2:])})")
					if inspect.iscoroutinefunction(getattr(self.agent, body[1])):
						await fn(self)
					else:
						fn(self)
				else:
					print(f"No function {body[1]} on {self.agent.jid}.")
			elif body[0] == 'disablemsg':
				for b in self.agent.behaviours:
					b.disableMessages()
			elif body[0] == 'enablemsg':
				for b in self.agent.behaviours:
					b.enableMessages()
			elif body[0] == 'set' or body[0] == 'sethold':
				print ("Setting next measurement value!")
				self.agent.setNextMeasurementValue(int(body[1]), body[0] == 'sethold')
			elif body[0] == 'stop':
				if self.agent.agentname[1] in ['A', 'B', 'C', 'D']:
					self.agent.port.float()
					for b in self.agent.behaviours:
						b.disableMessages()
				elif self.agent.agentname[1] in ['1', '2', '3', '4']:
					for b in self.agent.behaviours:
						b.disableMessages()
			elif body[0] == 'getinfo':
				message = spade.message.Message(
					to=agentnames.error,
					thread="1",
					metadata = {"type": "info"},
					body=f"{self.agent.jid} info:\n{self.agent.getInfo()}\n"
				)
				await self.send(message)
								
		else:
			print("Control behaviour received no message, but receive call ended")


class CyclicBehaviour(spade.behaviour.CyclicBehaviour):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.templates = []
		self.messagesEnabled = True
	
	async def send(self, msg):
		if self.messagesEnabled: 
			await super().send(msg)

	def enableMessages(self):
		self.messagesEnabled = True

	def disableMessages(self):
		self.messagesEnabled = False
	

	def createMasterTemplate(self):
		master = self.templates[0][0]
		for i in range(1, len(self.templates)):
			master = spade.template.ORTemplate(master, self.templates[i][0])
		self.set_template(master)
	async def on_start(self):
		self.templates.append((None, self.logUnprocessedMessage))
	
	async def run(self):
		msg = await self.receive(timeout = 5)
		if msg:
			if not msg.sender == agentnames.control:
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
			else:
				print("Normal behaviour received msg from control agent.")
				print("Check templates to ensure this message disappears.")
	async def logUnprocessedMessage(self, msg):
		message = spade.message.Message(
			to = agentnames.error,
			thread = "1",
			metadata = {"type": "unprocessed"},
			body = f"{self.agent.jid} received a message from {msg.sender} that it could not process:\n{msg.body}"
		)
		await self.send(message)
	async def logError(self, msg):
		message = spade.message.Message(
			to=agentnames.error,
			thread="1",
			metadata = {"type": "error"},
			body=f"{self.agent.jid} encountered the following error:\n{msg}"
		)
		await self.send(message)
	
	async def logInfo(self, msg):
		message = spade.message.Message(
			to = agentnames.error,
			thread = "2",
			metadata = {"type": "info"},
			body = msg
		)
		await self.send(message)
		
class OneShotBehaviour(spade.behaviour.OneShotBehaviour):
	async def logUnprocessedMessage(self, msg):
		message = spade.message.Message(
			to = agentnames.error,
			thread = "1",
			metadata = {"type": "unprocessed"},
			body = f"{self.agent.jid} received a message from {msg.sender} that it could not process:\n{msg.body}"
		)
		await self.send(message)
	async def logError(self, msg):
		message = spade.message.Message(
			to=agentnames.error,
			thread="1",
			metadata = {"type": "error"},
			body=f"{self.agent.jid} encountered the following error:\n{msg}"
		)
		await self.send(message)
	
	async def logInfo(self, msg):
		message = spade.message.Message(
			to = agentnames.error,
			thread = "2",
			metadata = {"type": "info"},
			body = msg
		)
		await self.send(message)

# Must be a way to avoid the code duplication, but no free functions makes it a little hard.
# JUst duplicating is simple.