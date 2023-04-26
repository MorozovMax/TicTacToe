"""
Module for automation of the assembly process
"""

import glob
from typing import Dict, Any
import tomli


DOIT_CONFIG = {'default_tasks': ['all'],
               'exclude': ['gitclean', 'wheel']}


def dumpkeys(infile: str, table: str, outfile: str) -> None:
    """
    Dumps TOML table keys one per line.

    :param infile: input file name
    :type infile: class: `str`
    :param table: section name in input file
    :type table: class: `str`
    :param outfile: output file name
    :type outfile: class: `str`
    """
    with open(infile, "rb") as fin:
        full = tomli.load(fin)
    with open(outfile, "w") as fout:
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
        'actions': ['sphinx-build -M html doc build'],
    }


def task_pot() -> Dict[str, Any]:
    """
    Re-create .pot file.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['pybabel extract -o tictactoe.pot app/*.py'],
        'file_dep': glob.glob('app/*.py'),
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
        'actions': ['pybabel compile -D tictactoe -l ru -i locale/ru/LC_MESSAGES/tictactoe.po -d locale'],
        'file_dep': ['locale/ru/LC_MESSAGES/tictactoe.po'],
        'targets': ['locale/ru/LC_MESSAGES/tictactoe.mo'],
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
        'actions': ['python -m build -n -w'],
        'task_dep': ['mo', 'requirements'],
    }


def task_style_flake() -> Dict[str, Any]:
    """
    Check style against flake8.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['flake8 app/authentification_page.py', 'flake8 app/game_page.py',
                    'flake8 app/search_game_page.py', 'flake8 app/setting_page.py',
                    'flake8 app/start_page.py', 'flake8 app/tictactoe.py', 'flake8 server.py',
                    'flake8 dodo.py']
    }


def task_style_pylint() -> Dict[str, Any]:
    """
    Check style against pylint.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['pylint app/authentification_page.py', 'pylint app/game_page.py',
                    'pylint app/search_game_page.py', 'pylint app/setting_page.py',
                    'pylint app/start_page.py', 'pylint app/tictactoe.py', 'pylint server.py',
                    'pylint dodo.py']
    }


def task_docstyle() -> Dict[str, Any]:
    """
    Check docstrings against pydocstyle.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': ['pydocstyle app/authentification_page.py', 'pydocstyle app/game_page.py',
                    'pydocstyle app/search_game_page.py', 'pydocstyle app/setting_page.py',
                    'pydocstyle app/start_page.py', 'pydocstyle app/tictactoe.py', 'pydocstyle server.py',
                    'pydocstyle dodo.py']
    }


def task_check() -> Dict[str, Any]:
    """
    Perform all checks.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': None,
        'task_dep': ['style_flake', 'docstyle', 'style_pylint']
    }


def task_all() -> Dict[str, Any]:
    """
    Perform all build tasks.

    :return: managing dictionary
    :rtype: class `Dict[str, Any]`
    """
    return {
        'actions': None,
        'task_dep': ['check', 'html', 'wheel']
    }
