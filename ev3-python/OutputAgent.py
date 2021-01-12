from MyAgent import MyAgent
import subprocess
from MyBehaviour import CyclicBehaviour
import spade
import agentnames
from PiStorms import PiStorms
class OutputAgent(MyAgent):
	class Behaviour(CyclicBehaviour):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.templates.append((spade.template.Template(), self.playConfirmSound))
			self.templates[-1][0].body = 'ready'
			self.templates.append((spade.template.Template(), self.displayDropError))
			self.templates[-1][0].body = 'incorrect brick'
			self.templates.append((spade.template.Template(), self.displaySortText))
			self.templates[-1][0].body = 'sort'
			self.templates.append((spade.template.Template(), self.displayShredAndWash))
			self.templates[-1][0].body = 'brick dropped'
			self.templates.append((spade.template.Template(), self.displayColorError))
			self.templates[-1][0].body = 'color error'
			self.templates.append((spade.template.Template(), self.displayBuildText))
			self.templates[-1][0].body = 'build'
			self.templates.append((spade.template.Template(), self.displayEjectText))
			self.templates[-1][0].body = 'eject'
			self.templates.append((spade.template.Template(), self.startNoTouchErrorSound))
			self.templates[-1][0].body = 'proximity alert'
			self.templates.append((spade.template.Template(), self.stopNoTouchErrorSound))
			self.templates[-1][0].body = 'area clear'
			self.templates.append((spade.template.Template(), self.startColorErrorSound))
			self.templates[-1][0].body = 'color error'
			self.templates.append((spade.template.Template(), self.stopColorErrorSound))
			self.templates[-1][0].body = 'color correct'
			self.templates.append((spade.template.Template(), self.sortColorErrorMessageAndSound))
			self.templates[-1][0].body = 'sort color error'
			self.templates.append((spade.template.Template(), self.displayColorChooser))
			self.templates[-1][0].body = 'next brick'
		async def displayColorChooser(self):
			pass # Not yetimplemented, see SensorAgent11.py
		async def displayShredAndWash(self):
			await self.displayShredding()
			await self.displayWashing()
		async def displayNoTouch(self, clear=True, col=1, row=5):
			text = [' ' * col, 'NO TOUCHY!']
			self.__displayText(clear, ''.join(text), row)

		async def sortColorErrorMessageAndSound(self):
			await self.displayColorError()
			await self.playColorErrorSound()

		async def displayShredding(self, clear=True, col=2, row=5):
			text = [' ' * col, 'SHREDDING']
			self.__displayText(clear, ''.join(text), row)

		async def displayWashing(self, clear=False, col=3, row=7):
			text = [' ' * col, 'WASHING']
			self.__displayText(clear, ''.join(text), row)

		async def displayColorError(self, clear=True, col=0, row=5):
			text = [' ' * col, 'COLOR ERROR']
			self.__displayText(clear, ''.join(text), row)

		async def displayBuildText(self, clear=True, col=0, row=5):
			text = [' ' * col, 'STACKING...'] # I guess? Not in pseudo code -> TODO
			self.__displayText(clear, ''.join(text), row)

		async def displayEjectText(self, clear=True, col=0, row=5):
			text = [' ' * col, 'EJECTING']
			self.__displayText(clear, ''.join(text), row)
		
		async def displaySortText(self, clear=True, col=0, row=5):
			text = [' ' * col, 'SORTING...']
			self.__displayText(clear, ''.join(text), row)

		async def displayDropError(self, clear=True, col=1, row=5):
			text = [' ' * col, 'DROP ERROR']
			self.__displayText(clear, ''.join(text), row)

		def __displayText(self, clear, text, line):
			if clear:
				self.agent.psm.screen.clearScreen(True)
			self.agent.psm.screen.termPrintAt(line, text)

	# For these, we either have a pip dependency or a system dependency
	# Setup script for PiStorms install mpg123, which can play sound files
	# So we use that to play ours as well. 
		async def startNoTouchErrorSound(self):
			pass
			# TODO
			# assert self.touchErrorProcess is None
			# # Path needs to be corrected
			# self.touchErrorProcess = self.__playAudioFile('~/touch_error.wav')
		async def stopNoTouchErrorSound(self):
			pass
			# TODO
			# assert self.touchErrorProcess is not None
			# self.__stopAudio(self.touchErrorProcess)
			# self.touchErrorProcess = None

		async def startColorErrorSound(self):
			pass
			# TODO
			# assert self.colorErrorProcess is None
			# Path needs to be corrected
			# self.colorErrorProcess = self.__playAudioFile('~/color_error.wav')
		async def stopColorErrorSound(self):
			pass
			# TODO
			#self.__stopAudio(self.colorErrorProcess)
			#self.colorErrorProcess = None

		async def playConfirmSound(self):
			# Discard return because we don't loop
			# So don't need to manually kill the process
			self.__playAudioFile('~/confirm.wav', False)

		async def playColorErrorSound(self):
			self.__playAudioFile('~/color_error.wav', False)

		def __playAudioFile(self, file, loop=True):
			pass
			#return subprocess.Popen(['mpg123', file, '--loop -1' if loop else ''])

		def __stopAudio(self, proc):
			proc.terminate()
	
	
	
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.psm = PiStorms()
		self.touchErrorProcess = None
		self.colorErrorProcess = None
		self.add_behaviour(self.Behaviour())


	

def createOutputAgent():
	return OutputAgent(agentnames.output, "output")