import bottle
import os

from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from play import Play






@bottle.post('/start')
def start():
    Play.score = 0
    Play.candy_in_pocket_enemy = 0
    Play.candy_in_pocket_self = 0
    return "Ghosty the Gatekeeper"


@bottle.post('/chooseAction')
def move():
    data = PublicGameState(ext_dict=bottle.request.json)
    pos00 = int(data.publicPlayers[0]['position'][1])
    data.publicPlayers[0]['position'][1] = int(data.publicPlayers[0]['position'][0])
    data.publicPlayers[0]['position'][0] = pos00
    pos10 = int(data.publicPlayers[1]['position'][1])
    data.publicPlayers[1]['position'][1] = int(data.publicPlayers[1]['position'][0])
    data.publicPlayers[1]['position'][0] = pos10
    side = data.agent_id
    my_player = PublicPlayer(jsonString=data.publicPlayers[side])
    enemy = PublicPlayer(jsonString=data.publicPlayers[(side + 1) % 2])

    field = data.gameField
    return Play(side, field, my_player, enemy).take_turn()


application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', 'localhost'), port=os.getenv('PORT', '8080'))