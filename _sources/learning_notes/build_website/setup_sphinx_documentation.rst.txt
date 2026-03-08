Setting Up Sphinx Documentation for Phibui Robotics Lab
=======================================================

Overview
--------

In Phase 2 of the **phibui-robotics** project, the goal was to set up a
documentation system for the website **Phibui Robotics Lab** using **Sphinx**
and **reStructuredText (RST)**.

The documentation system allows all robotics projects, tutorials, learning
notes, and blog posts to be written as structured documentation and
automatically converted into a static HTML website.

This phase focused on building the **documentation engine** that will power
the website.

Development Environment
-----------------------

Operating System:

- Ubuntu 22.04

Documentation stack:

- Sphinx
- reStructuredText (.rst)
- sphinx_rtd_theme
- Python virtual environment

Project structure:

::

   phibui-robotics
   │
   ├── docs-env
   │
   ├── docs
   │   │
   │   ├── build
   │   ├── source
   │   │
   │   │   ├── projects
   │   │   ├── tutorials
   │   │   ├── learning_notes
   │   │   └── blog
   │   │
   │   │   ├── index.rst
   │   │   └── conf.py
   │   │
   │   ├── Makefile
   │   └── make.bat
   │
   ├── ros2_ws
   ├── firmware
   ├── hardware
   ├── simulations
   └── scripts

Key Steps in Phase 2
--------------------

1. Create a Python virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A dedicated Python environment was created to isolate the documentation
dependencies from the system Python.

Command used:

::

   python3 -m venv docs-env

Activate the environment:

::

   source docs-env/bin/activate

This ensures that Sphinx and its dependencies are installed locally
within the project.

2. Install Sphinx
~~~~~~~~~~~~~~~~~

Sphinx is the documentation generator that converts RST files into HTML.

Installation command:

::

   pip install sphinx

After installation, the version can be checked with:

::

   sphinx-build --version

3. Install Documentation Theme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **ReadTheDocs theme** was installed to provide a professional-looking
documentation interface.

Command:

::

   pip install sphinx_rtd_theme

The theme was then configured inside the file:

::

   docs/source/conf.py

by modifying:

::

   html_theme = 'sphinx_rtd_theme'

4. Initialize the Sphinx Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sphinx was initialized using the command:

::

   sphinx-quickstart

During initialization the option **separate source and build directories**
was enabled.

This generated the following files:

- ``conf.py`` – configuration file for Sphinx
- ``index.rst`` – the homepage of the documentation
- ``Makefile`` – build automation script
- ``build/`` – output directory for generated HTML

5. Organize Documentation Sections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The documentation was divided into four main sections:

- Projects
- Tutorials
- Learning Notes
- Blog

Each section contains its own ``index.rst`` file.

Example structure:

::

   docs/source/tutorials/index.rst
   docs/source/projects/index.rst
   docs/source/learning_notes/index.rst
   docs/source/blog/index.rst

Each section acts as a **documentation hub** for related pages.

6. Configure Navigation with Toctree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sphinx uses the ``toctree`` directive to build the website navigation.

Example in ``index.rst``:

::

   .. toctree::
      :maxdepth: 2
      :caption: Contents

      projects/index
      tutorials/index
      learning_notes/index
      blog/index

This creates the sidebar navigation menu.

7. Build the Documentation Website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The documentation was compiled into HTML using:

::

   make html

This command internally runs:

::

   sphinx-build -b html source build/html

The generated website is located at:

::

   docs/build/html/index.html

The site can be opened in a browser using:

::

   xdg-open build/html/index.html

Key Files and Their Roles
-------------------------

conf.py
~~~~~~~

The main configuration file for Sphinx.

Responsible for:

- project metadata
- theme configuration
- extensions
- static files
- build settings

index.rst
~~~~~~~~~

The main entry point of the documentation website.

It defines:

- homepage content
- main navigation structure
- documentation hierarchy

Makefile
~~~~~~~~

A helper script used to simplify build commands.

Examples:

::

   make html
   make clean

This eliminates the need to manually run ``sphinx-build``.

Important Concepts Learned
--------------------------

Virtual Environments
~~~~~~~~~~~~~~~~~~~~

Using a Python virtual environment ensures that documentation tools are
isolated from the system Python and other projects.

Sphinx Documentation System
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sphinx is a powerful static documentation generator widely used in
engineering and software projects.

Examples include:

- Python documentation
- ROS documentation
- NVIDIA developer documentation

reStructuredText (RST)
~~~~~~~~~~~~~~~~~~~~~~

RST is a markup language designed for technical documentation.

Features include:

- structured headings
- automatic table of contents
- code blocks
- cross references
- extensible directives

Documentation Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~

The documentation was structured into modular sections:

- project documentation
- tutorials
- learning notes
- blog posts

This structure allows the documentation to scale as the robotics project
grows.

Outcome of Phase 2
------------------

At the end of this phase:

- A complete Sphinx documentation system was created.
- The **Phibui Robotics Lab** website successfully builds locally.
- Documentation can now be written using structured RST files.
- The project now has a scalable documentation architecture.

Next Phase
----------

The next step is to deploy the documentation website using:

- GitHub Pages
- GitHub Actions

This will enable **automatic deployment** of the website whenever new
documentation is pushed to the repository.