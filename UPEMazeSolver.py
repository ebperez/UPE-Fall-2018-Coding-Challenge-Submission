import requests
import json

def maze():
	# Prompt for UID
	uidNum = input('Enter your UID: ')

	# Get the Token by posting my UID
	url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session'
	payload = {'uid':str(uidNum)}
	headers = {'Accept':'application/x-www-form-url','Content-type':'application/json'}
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	token = r.json()['token']
	
	session = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token
	r = requests.get(session)

	totalLevels = r.json()['total_levels']
	levelsCompleted = r.json()['levels_completed']	
	
	# Possible moves
	left = {'action':'LEFT'}
	right = {'action':'RIGHT'}
	up = {'action':'UP'}
	down = {'action':'DOWN'}

	# Solve all the levels
	while levelsCompleted < totalLevels:
		r = requests.get(session)
		print r.json()
		mazeSize = r.json()['maze_size']
		cols = mazeSize[0]
		rows = mazeSize[1]

		coords = r.json()['current_location']
		xPos = coords[0]
		yPos = coords[1]

		# Initialized visited matrix to mark as visited
		visited = [[False for j in range(cols)] for i in range(rows)]
		
		# Solves the maze and returns whether or not a path to the end has been found
		def solve(x, y):
			visited[y][x] = True
			# UP
			# If it is out of bounds, visited, or a wall don't recurse down that path
			if y - 1 >= 0 and visited[y - 1][x] is False:
				outcome = move(up, session, headers)
				if outcome == 'END':
					return True
				elif outcome == 'SUCCESS':
					# Recurse
					solved = solve(x, y - 1)
					if solved is True:
						return True
					# Backtrack
					move(down, session, headers)
				elif outcome == 'WALL':
					visited[y - 1][x] = True

			# DOWN
			# If it is out of bounds, visited, or a wall don't recurse down that path
			if y + 1 < rows and visited[y + 1][x] is False:
				outcome = move(down, session, headers)
				if outcome == 'END':
					return True
				elif outcome == 'SUCCESS':
					# Recurse
					solved = solve(x, y + 1)
					if solved is True:
						return True
					# Backtrack
					move(up, session, headers)
				elif outcome == 'WALL':
					visited[y + 1][x] = True

			# LEFT
			# If it is out of bounds, visited, or a wall don't recurse down that path
			if x - 1 >= 0 and visited[y][x - 1] is False:
				outcome = move(left, session, headers)
				if outcome == 'END':
					return True
				elif outcome == 'SUCCESS':
					# Recurse
					solved = solve(x - 1, y)
					if solved is True:
						return True
					# Backtrack
					move(right, session, headers)
				elif outcome == 'WALL':
					visited[y][x - 1] = True

			# RIGHT
			# If it is out of bounds, visited, or a wall don't recurse down that path
			if x + 1 < cols and visited[y][x + 1] is False:
				outcome = move(right, session, headers)
				if outcome == 'END':
					return True
				elif outcome == 'SUCCESS':
					# Recurse
					solved = solve(x + 1, y)
					if solved is True:
						return True
					# Backtrack
					move(left, session, headers)
				elif outcome == 'WALL':
					visited[y][x + 1] = True

			return False

		# Recursively solve the current
		solve(xPos, yPos)
		levelsCompleted += 1

	r = requests.get(session)
	print r.json()


# Moves your position in the specified direction
def move(direction, session, header):
	return requests.post(session, data = json.dumps(direction), headers = header).json()['result']

# Solve all the mazes
maze()
