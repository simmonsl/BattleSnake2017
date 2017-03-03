import bottle
import os
import random

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
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]

    for snake in data['snakes']:
        if snake['id'] == data['you']:
            mysnake = snake
        for coord in snake['coords']:
            grid[coord[0]][coord[1]] = SNAKE_BODY
        #grid[snake['coords'][0]] = SNAKE_HEAD

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

    return mysnake, grid


def get_available_moves(data, grid, mysnake):
    directions = []

    head = mysnake['coords'][0]
    up = [head[0], head[1] + 1]
    down = [head[0], head[1] - 1]
    left = [head[0] - 1, head[1]]
    right = [head[0] + 1, head[1]]

    if not (up[1] < 0 or up[1] > data['height'] or grid[up[0]][up[1]] > 1):
        directions.append('up')
        #directions.remove(directions.index('up'))
    if not (down[1] < 0 or down[1] > data['height'] or grid[down[0]][down[1]] > 1):
        directions.append('down')
       # directions.remove(directions.index('down'))
    if not (left[0] < 0 or left[0] > data['width'] or grid[left[0]][left[1]] > 1):
        directions.append('left')
       # directions.remove(directions.index('left'))
    if not (right[0] < 0 or right[0] > data['width'] or grid[right[0]][right[1]] > 1):
        directions.append('right')
      #  directions.remove(directions.index('right'))

    return directions

@bottle.post('/move')
def move():
    data = bottle.request.json
    # TODO: Do things with data
    mysnake, grid = init(data)
    directions = get_available_moves(data, grid, mysnake)

    return {
        'move': random.choice(directions),
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', 'localhost'), port=os.getenv('PORT', '8080'))
