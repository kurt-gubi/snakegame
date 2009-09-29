import subprocess

class BotWrapper(object):
    def __init__(self, process):
        self.process = process

    def __call__(self, board, (x, y)):
        height = len(board)
        width = len(board[0])

        letter = board[y][x].lower()

        proc = subprocess.Popen(
            [self.process],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        board = '\n'.join([''.join(row) for row in board])

        print>>proc.stdin, width, height, letter
        print>>proc.stdin, board
        proc.stdin.close()
        proc.wait()

        assert proc.returncode == 0, 'Snake died.'
        output = proc.stdout.read()
        return output.strip()

