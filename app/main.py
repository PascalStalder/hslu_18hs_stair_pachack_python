import random
import bottle
import os

from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections
from play import Play

side = None



@bottle.post('/start')
def start():

    # todo: set dynamically
    side = 0
    return "SomeFancyTeamName"


@bottle.post('/chooseAction')
def move():
    data = PublicGameState(ext_dict=bottle.request.json)

    side = data.agent_id
    players = data.publicPlayers
    my_player = PublicPlayer(jsonString=data.publicPlayers[side])
    enemy = PublicPlayer(jsonString=data.publicPlayers[side + 1 % 2])
    field = data.gameField
    return Play(side, field, my_player, enemy).take_turn()


application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', 'localhost'), port=os.getenv('PORT', '8080'))