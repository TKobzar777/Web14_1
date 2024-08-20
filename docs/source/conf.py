import sys
import os
# Определяем абсолютный путь к корневому каталогу проекта
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Добавляем путь к корневому каталогу в sys.path
sys.path.insert(0, project_root)
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'REST ARI CONTACT'
copyright = '2024, Tetiana Kobzar'
author = 'Tetiana Kobzar'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []
#
# templates_path = ['_templates']
# exclude_patterns = []
extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']

