"""Module for automation of the assembly process."""

import glob
from typing import Dict, Any
import tomli
from doit.tools import create_folder


DOIT_CONFIG = {'default_tasks': ['all']}


def dumpkeys(infile: str, table: str, outfile: str) -> None:
    """
    Dump TOML table keys one per line.

    :param infile: input file name
    :type infile: class: `str`
    :param table: section name in input file
    :type table: class: `str`
    :param outfile: output file name
    :type outfile: class: `str`
    """
    with open(infile, "rb") as fin:
        full = tomli.load(fin)
    with open(outfile, "w", encoding='utf-8') as fout:
        print(*full[table], sep="\n", file=fout)


def task_gitclean() -> Dict[str, Any]:
    """
    Clean all generated files not tracked by GIT.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['git clean -xdf'],
    }


def task_html() -> Dict[str, Any]:
    """
    Make HTML documentation.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['sphinx-build -M html doc build']
    }


def task_pot() -> Dict[str, Any]:
    """
    Re-create .pot file.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['pybabel extract -o tictactoe.pot OnlineTicTacToe/*.py'],
        'file_dep': glob.glob('OnlineTicTacToe/*.py'),
        'targets': ['tictactoe.pot'],
    }


def task_po() -> Dict[str, Any]:
    """
    Update translations.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['pybabel update -D tictactoe -d locale -i tictactoe.pot'],
        'file_dep': ['tictactoe.pot'],
        'targets': ['locale/ru/LC_MESSAGES/tictactoe.po'],
    }


def task_mo() -> Dict[str, Any]:
    """
    Compile translations.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
      'actions': [(create_folder, ['OnlineTicTacToe/locale/ru/LC_MESSAGES']),
                  'pybabel compile -D tictactoe -l ru -i locale/ru/LC_MESSAGES/tictactoe.po -d OnlineTicTacToe/locale'],
      'file_dep': ['locale/ru/LC_MESSAGES/tictactoe.po'],
      'targets': ['OnlineTicTacToe/locale/ru/LC_MESSAGES/tictactoe.mo'],
    }


def task_create_setup() -> Dict[str, Any]:
    """
    Create Setup file.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['cp setup/OnlineTicTacToe.spec TicTacToe',
                    'pyinstaller --distpath setup/dist --workpath setup/build setup/setup.spec',
                    'mv setup/dist/Setup TicTacToe/Setup'],
        'file_dep': ['setup/OnlineTicTacToe.spec', 'setup/setup.py', 'setup/setup.spec'],
        'task_dep': ['wheel'],
        'targets': ['TicTacToe/Setup', 'TicTacToe/OnlineTicTacToe.spec'],
    }


def task_create_arch() -> Dict[str, Any]:
    """
    Create archive with setup distributive.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['tar -czvf OnlineTicTacToe.tar.gz TicTacToe',
                    'mv TicTacToe/*.whl .'],
        'task_dep': ['create_setup'],
        'targets': ['OnlineTicTacToe.tar.gz'],
    }


def task_requirements() -> Dict[str, Any]:
    """
    Dump Pipfile requirements.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
            'actions': [(dumpkeys, ["Pipfile", "packages", "requirements.txt"])],
            'file_dep': ['Pipfile'],
            'targets': ['requirements.txt'],
           }


def task_wheel() -> Dict[str, Any]:
    """
    Create binary wheel distribution.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': [(create_folder, ['TicTacToe']),
                    'python -m build -n -w',
                    'mv dist/*.whl TicTacToe'],
        'task_dep': ['mo', 'requirements'],
    }


def task_style_flake() -> Dict[str, Any]:
    """
    Check style against flake8.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['flake8 OnlineTicTacToe/authentification_page.py', 'flake8 OnlineTicTacToe/game_page.py',
                    'flake8 OnlineTicTacToe/search_game_page.py', 'flake8 OnlineTicTacToe/setting_page.py',
                    'flake8 OnlineTicTacToe/start_page.py', 'flake8 OnlineTicTacToe/tictactoe.py',
                    'flake8 server_dir/server.py', 'flake8 dodo.py', 'flake8 setup/setup.py',
                    'flake8 OnlineTicTacToe/__main__.py']
    }


def task_style_pylint() -> Dict[str, Any]:
    """
    Check style against pylint.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['pylint OnlineTicTacToe/authentification_page.py', 'pylint OnlineTicTacToe/game_page.py',
                    'pylint OnlineTicTacToe/search_game_page.py', 'pylint OnlineTicTacToe/setting_page.py',
                    'pylint OnlineTicTacToe/start_page.py', 'pylint OnlineTicTacToe/tictactoe.py',
                    'pylint server_dir/server.py', 'pylint dodo.py', 'pylint setup/setup.py',
                    'pylint OnlineTicTacToe/__main__.py']
    }


def task_docstyle() -> Dict[str, Any]:
    """
    Check docstrings against pydocstyle.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['pydocstyle OnlineTicTacToe/authentification_page.py', 'pydocstyle OnlineTicTacToe/game_page.py',
                    'pydocstyle OnlineTicTacToe/search_game_page.py', 'pydocstyle OnlineTicTacToe/setting_page.py',
                    'pydocstyle OnlineTicTacToe/start_page.py', 'pydocstyle OnlineTicTacToe/tictactoe.py',
                    'pydocstyle server_dir/server.py', 'pydocstyle dodo.py', 'pydocstyle setup/setup.py',
                    'pydocstyle OnlineTicTacToe/__main__.py']
    }


def task_check() -> Dict[str, Any]:
    """
    Perform all checks.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': None,
        'task_dep': ['style_flake', 'style_pylint', 'docstyle']
    }


def task_all() -> Dict[str, Any]:
    """
    Perform all build tasks.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': None,
        'task_dep': ['html', 'check', 'create_arch']
    }


def task_run_server() -> Dict[str, Any]:
    """
    Run server.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['sudo docker compose -f server_dir/docker-compose.yml up -d'],
        'file_dep': ['server_dir/server.py',
                     'server_dir/run_server.sh',
                     'server_dir/Pipfile',
                     'server_dir/Dockerfile',
                     'server_dir/docker-compose.yml'],
        'uptodate': [False]
    }


def task_stop_server() -> Dict[str, Any]:
    """
    Stop server.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['docker stop tictactoe_server'],
        'uptodate': [False]
    }
