from __future__ import absolute_import

import pickle

class Viewer(object):
    def __init__(self, engine, sock):
        self.sock = sock
        self.engine = engine

    def run(self):
        for board in self.engine:
            bots = {
                letter: (None, colour, None, team)
                for letter, (_, colour, _, team) in self.engine.bots.iteritems()
            }

            msg = pickle.dumps({
                'bots': bots,
                'board': board,
            }, protocol=2)

            self.sock.send(msg)

class Engine(object):
    def __init__(self, sock):
        self.sock = sock

    def __iter__(self):
        while True:
            if not self.sock.poll(timeout=2000):
                break
            msg = self.sock.recv()
            obj = pickle.loads(msg)
            self.bots = obj['bots']
            yield obj['board']
