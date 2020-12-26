from MotorAgent import MotorAgent
import time
import spade
from MyBehaviour import OneShotBehaviour, CyclicBehaviour
MotorAgent1AName = "agent1A@192.168.1.8"
class MotorAgent1A(MotorAgent):
	class Behaviour_start(OneShotBehaviour):
		async def run(self): # R_DRP
			self.agent.port.setSpeed(8)
			time.sleep(0.5)
			self.agent.port.waitUntilNotBusy()
			self.agent.port.runDegs(degs=-90, speed=50, brakeOnCompletion=True)
			self.agent.resetRotation()

	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates.append((spade.template.Template(), self.drop))
			self.templates[-1][0].body = "brick ready"
			self.createMasterTemplate()

		async def drop(self):
			degrees = -70 - self.agent.readRotation()
			self.agent.port.runDegs(degs=degrees, speed=10, brakeOnCompletion=True)
			degrees = -1 * self.agent.readRotation()
			self.agent.port.runDegs(degs=degrees, speed=20, brakeOnCompletion=True)
			# Send to everyone in Shred()
			msg = spade.message.Message()
			msg.to = 'output@192.168.1.8'
			msg.body = 'brick dropped'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = 'agent1B@192.168.1.8'
			msg.body = 'brick dropped'
			await self.send(msg)
			msg = spade.message.Message()
			msg.to = 'agent1C@192.168.1.8'
			msg.body = 'brick dropped'
			await self.send(msg)
			# Brief pause to maintain correct order
			# Probably not necessary, but eh
			time.sleep(0.1)
			# And continue onwards in the loop. 
			# Barrier might pause shred, but will resume it afterwards. 
			msg = spade.message.Message()
			msg.to = 'agent13@192.168.1.8'
			msg.body = 'proximity check'
			await self.send(msg)

		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.agentname = "1A"
		self.add_behaviour(self.Behaviour_start())
		self.add_behaviour(self.Behaviour())

 
def createAgent1A():
	agent = MotorAgent1A(MotorAgent1AName, "agent1A")
	return agent

# from PiStorms import PiStorms
# from spade import agent
# from spade import quit_spade
# import time

# class DummyAgent(agent.Agent):
#     async def setup(self):
#         print("Hello World! I'm agent {}".format(str(self.jid)))
#         psm = PiStorms()
#         psm.screen.termPrintln("EV3 Motor and US Sensor test")
#         psm.BAM1.runDegs(360, 75, True, False)
#         dist = psm.BAS1.distanceUSEV3()
#         print(dist)
#         psm.screen.clearScreen()
#         psm.screen.Text(str(drawAutodist), 35, 200, fill=(255, 255, 255), size = 18)
			
# dummy = DummyAgent("challenger@jabber.de", "123456")
# dummy.start()
# time.sleep(10)
# dummy.stop()
# quit_spade()