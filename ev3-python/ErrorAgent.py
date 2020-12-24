import spade

class ErrorAgent(spade.agent.Agent):
  class LogBehaviour(spade.behaviour.CyclicBehaviour):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

    async def run(self):
      msg = await self.receive(timeout = 5)
      if msg:
        print(f"Error encountered by an agent:\n{msg.body}")
      else:
        pass # No errors logged
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  async def setup(self):
    self.add_behaviour(self.LogBehaviour())
  
def createErrorAgent():
  return ErrorAgent("error@192.168.1.8", "error")