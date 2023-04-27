import os


if __name__ == '__main__':
    cur_dir = os.getcwd()

    os.mkdir('/tmp/TicTacToe-install')
    os.chdir('/tmp/TicTacToe-install')

    os.system('python3 -m venv myappenv')

    os.system('myappenv/bin/python -m pip install pyinstaller')
    os.system('cp ' + cur_dir + "/TicTacToe/*.whl" + ' ' + os.getcwd())

    os.system('myappenv/bin/python -m pip install *.whl')

    os.system('cp ' + cur_dir + "/TicTacToe/OnlineTicTacToe.spec" + ' ' + os.getcwd())

    os.system('myappenv/bin/python -m PyInstaller OnlineTicTacToe.spec')

    os.mkdir('/tmp/OnlineTicTacToeGame')

    os.system('mv dist/OnlineTicTacToe /tmp/OnlineTicTacToeGame/OnlineTicTacToe')

    os.chdir(cur_dir)

    os.system('rm -rf /tmp/TicTacToe-install')
