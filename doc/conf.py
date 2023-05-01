# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys


sys.path.insert(0, os.path.abspath('../OnlineTicTacToe'))
sys.path.insert(0, os.path.abspath('../server_dir'))
sys.path.insert(0, os.path.abspath('../setup'))
sys.path.insert(0, os.path.abspath('../'))

project = 'Online TicTacToe'
copyright = '2023, Pavlishin Kirill, Morozov Maksim'
author = 'Pavlishin Kirill, Morozov Maksim'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

autodoc_default_options = {
    'members': True,
    'private-members': True,
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'agogo'
html_static_path = ['_static']
