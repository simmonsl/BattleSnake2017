import bottle
import os
import random
import AStar

FOOD = 1
SNAKE_BODY = 2
SNAKE_HEAD = 3

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }

def init(data):
    grid = [[0 for row in xrange(data['width'])] for col in xrange(data['height'])]

    for snake in data['snakes']:
        if snake['id'] == data['you']:
            mysnake = snake
        for coord in snake['coords']:
            grid[coord[0]][coord[1]] = SNAKE_BODY
        #grid[snake['coords'][0]] = SNAKE_HEAD

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

    return mysnake, grid

def get_food(data, grid, mysnake):
    foods = data['food']
    minDist = 100000

    for food in foods:
        potential_path = a_star(mysnake['coords'][0], food, grid, mysnake['coords'])
        if not potential_path:
            continue
        if dist < len(potential_path):
            minDist = dist
            path = potential_path

    return path

def get_available_moves(data, grid, mysnake):
    directions = []

    head = mysnake['coords'][0]
    up = [head[0], head[1] - 1]
    down = [head[0], head[1] + 1]
    left = [head[0] - 1, head[1]]
    right = [head[0] + 1, head[1]]

    if up[1] > 0 and up[1] < data['height'] and grid[up[0]][up[1]] <= 1:
        directions.append('up')
    if down[1] > 0 and down[1] < data['height'] and grid[down[0]][down[1]] <= 1:
        directions.append('down')
    if left[0] > 0 and left[0] < data['width'] and grid[left[0]][left[1]] <= 1:
        directions.append('left')
    if right[0] > 0 and right[0] < data['width'] and grid[right[0]][right[1]] <= 1:
        directions.append('right')

    return directions


@bottle.post('/move')
def move():
    data = bottle.request.json
    # TODO: Do things with data
    mysnake, grid = init(data)
    directions = get_available_moves(data, grid, mysnake)
    food = data['food']

    return {
        'move': random.choice(directions),
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', 'localhost'), port=os.getenv('PORT', '8080'))
