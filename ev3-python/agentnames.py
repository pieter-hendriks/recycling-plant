resource = 'dummy'
domain = '192.168.1.8'
agent1A = f'agent1A@{domain}/{resource}'
agent1B = f'agent1B@{domain}/{resource}'
agent1C = f'agent1C@{domain}/{resource}'
agent2B = f'agent2B@{domain}/{resource}'
agent2C = f'agent2C@{domain}/{resource}'
agent2D = f'agent2D@{domain}/{resource}'
agent11 = f'agent11@{domain}/{resource}'
agent12 = f'agent12@{domain}/{resource}'
agent13 = f'agent13@{domain}/{resource}'
agent14 = f'agent14@{domain}/{resource}'
output = f'output@{domain}/{resource}'
error = f'error@{domain}/{resource}'
control = f'control@{domain}/{resource}'

agentNames = [agent1A, agent1B, agent1C,
							agent2B, agent2C, agent2D,
							agent11, agent12, agent13, agent14]

miscAgentNames = [output, error, control]
allAgentNames = agentNames + miscAgentNames