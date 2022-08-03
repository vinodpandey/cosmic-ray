|Python version| |Python version windows| |Build Status| |Documentation|

Modifications to run Cosmic Ray on specific portion of a single file
====================================================================

Running mutation testing on whole codebase takes a long time. This activity can only be performed once in a while.
Developers need a solution which runs much faster and executed same as unit test.

In this modified code, we are able to execute mutation tests on specific portion of individual code file. Developers can
run this on selected method in a code file.

Before running mutation testing, make sure all changes are committed to respository. Source files are modified
during mutation testing and extra care should be taken to avoid accidently committing these changes to code repository.

Steps:

1. Install cosmic-ray

.. code-block::

   pip install -e git+https://github.com/vinodpandey/cosmic-ray@v1.0.0#egg=cosmic-ray

2. Create new config file (one time only)

.. code-block::

   cosmic-ray new-config cosmic-ray.toml

   [?] Top-level module path: apps/category/api/views.py
   [?] Test execution timeout (seconds): 10
   [?] Test command: python manage.py test --keepdb -v 2 category.tests.test_api_views.CategoryListTests
   -- MENU: Distributor --
   (0) http
   (1) local
   [?] Enter menu selection: 1

The above command creates a new config file with below data. The same config file can be used to
run different tests.

.. code-block::

   [cosmic-ray]
   module-path = "apps/category/api/views.py"
   timeout = 10.0
   excluded-modules = []
   test-command = "python manage.py test --keepdb -v 2 category.tests.test_api_views.CategoryListTests"

   [cosmic-ray.distributor]
   name = "local"

3. Initialization

.. code-block::

   cosmic-ray init cosmic-ray.toml cosmic-ray.sqlite

4. Baseline

.. code-block::

   cosmic-ray --verbosity=INFO baseline cosmic-ray.toml

5. Execution
Before executing below command, update cosmic-ray.toml to include start-limit and end-limit
which specifies the start and end line no. in the file for mutation testing scope.

.. code-block::

   [cosmic-ray]
   module-path = "apps/category/api/views.py"
   timeout = 10.0
   excluded-modules = []
   test-command = "python manage.py test --keepdb -v 2 category.tests.test_api_views.CategoryListTests"
   start-limit = 42
   end-limit = 60

   [cosmic-ray.distributor]
   name = "local"

Executing tests

.. code-block::

   cosmic-ray exec cosmic-ray.toml cosmic-ray.sqlite

Open a new terminal and run below command to check the progress

.. code-block::

   cr-report cosmic-ray.sqlite --show-pending

On test completion, run below command to generate html report

.. code-block::

   cr-html cosmic-ray.sqlite > report.html

For running the test again for different file or different line numbers:

1. Update config file with updated values for  `module-path` and `test-command`

2. Update `start-limit` and `start-limit` accordingly to limit testing scope

3. Delete existing `report.html` and `cosmic-ray.sqlite`

4. Continue with Initialization step (step 3) onwards


Cosmic Ray: mutation testing for Python
=======================================


   "Four human beings -- changed by space-born cosmic rays into something more than merely human."
   
   -- The Fantastic Four

Cosmic Ray is a mutation testing tool for Python 3.

It makes small changes to your source code, running your test suite for each
one. Here's how the mutations look:

.. image:: docs/source/cr-in-action.gif

|full_documentation|_

Contributing
------------

The easiest way to contribute is to use Cosmic Ray and submit reports for defects or any other issues you come across.
Please see CONTRIBUTING.rst for more details.

.. |Python version| image:: https://img.shields.io/badge/Python_version-3.5+-blue.svg
   :target: https://www.python.org/
.. |Python version windows| image:: https://img.shields.io/badge/Python_version_(windows)-3.7+-blue.svg
   :target: https://www.python.org/
.. |Build Status| image:: https://github.com/sixty-north/cosmic-ray/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/sixty-north/cosmic-ray/actions/workflows/python-package.yml
.. |Code Health| image:: https://landscape.io/github/sixty-north/cosmic-ray/master/landscape.svg?style=flat
   :target: https://landscape.io/github/sixty-north/cosmic-ray/master
.. |Code Coverage| image:: https://codecov.io/gh/sixty-north/cosmic-ray/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Vimjas/covimerage/branch/master
.. |Documentation| image:: https://readthedocs.org/projects/cosmic-ray/badge/?version=latest
   :target: http://cosmic-ray.readthedocs.org/en/latest/
.. |full_documentation| replace:: **Read the full documentation at readthedocs.**
.. _full_documentation: http://cosmic-ray.readthedocs.org/en/latest/
