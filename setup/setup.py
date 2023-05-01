"""Module which setup game to your operating system."""

import os
import subprocess
import glob


if __name__ == "__main__":
    cur_dir = os.getcwd()

    subprocess.run(['python3', '-m', 'venv', 'myappenv'], check=False)
    subprocess.run([f'{cur_dir}/myappenv/bin/python', '-m', 'pip', 'install', 'pyinstaller'], check=False)
    subprocess.run([f'{cur_dir}/myappenv/bin/python', '-m', 'pip', 'install', glob.glob(f'{cur_dir}/*.whl')[0]],
                   check=False)

    subprocess.run([f'{cur_dir}/myappenv/bin/python', '-m', 'PyInstaller', 'OnlineTicTacToe.spec'], check=False)

    os.mkdir(f'{cur_dir}/OnlineTicTacToeGame')

    subprocess.run(['mv', f'{cur_dir}/dist/OnlineTicTacToe', f'{cur_dir}/OnlineTicTacToeGame/OnlineTicTacToe'],
                   check=False)

    subprocess.run(['rm', '-rf', f'{cur_dir}/build'], check=False)
    subprocess.run(['rm', '-rf', f'{cur_dir}/dist'], check=False)
    subprocess.run(['rm', '-rf', f'{cur_dir}/myappenv'], check=False)
