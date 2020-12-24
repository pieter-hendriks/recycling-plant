from spade import agent
from spade import quit_spade
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.template import Template
from spade.message import Message
import spade
import time


class DummyRecvAgent(agent.Agent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, jid, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.jid = jid
			self.t = Template()
			self.t.metadata = {"performative": "inform"}
			self.t.sender = "agent1@192.168.1.8"
			self.t.body = "hello"
		async def run(self):
			message = await self.receive(timeout=10)
			if message:
				if self.t.match(message):
					print(f"Received {message.body}. Hello to you too!")
				else:
					print("Mismatched message")
			else:
				print("Time out, very lonely.")
		async def on_end(self):
			await self.agent.stop()
			
	async def setup(self):
		print(f"Agent {self.jid} setup!")
		self.add_behaviour(self.Behaviour(self.jid))


class DummySendAgent(agent.Agent):
	class Behaviour(PeriodicBehaviour):
		def __init__(self, jid, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.jid = jid
		async def run(self):
			print(f"Agent {self.jid}'s task is running once!")
			msg = Message(to="agent2@192.168.1.8")
			msg.body = "hello"
			msg.metadata = {"performative": "inform"}
			await self.send(msg)
		
		async def on_end(self):
			await self.agent.stop()

			
		
	async def setup(self):
		b = self.Behaviour(self.jid, period=1)
		self.add_behaviour(b)
			
send = DummySendAgent("agent1@192.168.1.8", "agent1")
recv = DummyRecvAgent("agent2@192.168.1.8", "agent2")
send.start()
recv.start()

time.sleep(3)

send.stop()
recv.stop()
quit_spade()