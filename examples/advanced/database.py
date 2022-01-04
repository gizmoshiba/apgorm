# MIT License
#
# Copyright (c) 2021 TrigonDev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from enum import IntEnum

import apgorm
from apgorm.constraints import ForeignKey
from apgorm.types.character import VarChar
from apgorm.types.numeric import Int, Serial


class PlayerStatus(IntEnum):
    NOT_FINISHED = 0
    WINNER = 1
    LOSER = 2
    DROPPED = 3


class PlayerStatusConverter(apgorm.Converter[int, PlayerStatus]):
    def to_stored(self, value: PlayerStatus) -> int:
        return int(value)

    def from_stored(self, value: int) -> PlayerStatus:
        return PlayerStatus(value)


class User(apgorm.Model):
    username = VarChar(32).field()
    nickname = VarChar(32).nullablefield(default="null")

    primary_key = (username,)


class Game(apgorm.Model):
    id_ = Serial().field()
    name = VarChar(32).field()

    primary_key = (id_,)


class Player(apgorm.Model):
    username = VarChar(32).field()
    game_id = Int().field()
    status = Int().field(default="0").with_converter(PlayerStatusConverter)

    username_fk = ForeignKey([username], [User.username])
    game_id_fk = ForeignKey([game_id], [Game.id_])
    primary_key = (
        username,
        game_id,
    )


class Database(apgorm.Database):
    users = User
    games = Game
    players = Player
