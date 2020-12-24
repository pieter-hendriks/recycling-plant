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
#         psm.screen.drawAutoText(str(dist), 35, 200, fill=(255, 255, 255), size = 18)
			
# dummy = DummyAgent("challenger@jabber.de", "123456")
# dummy.start()
# time.sleep(10)
# dummy.stop()
# quit_spade()


import PiStorms
import spade
import time


