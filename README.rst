|PyPI - Version| |GitHub License| |Pepy Total Downlods|

BELCH Password List Generator
=============================

BELCH Password List Generator is a simple tool to generate password
lists based on a given pattern. You can specify the password pattern and
generate multiple unique passwords.

Installation
------------

Install usig PIP:
~~~~~~~~~~~~~~~~~

.. code:: bash

   pip install belch 

Usage
-----

To generate passwords, run the following command from anywhere on your
system:

::

   belch 

Follow the on-screen instructions to specify the password pattern and
the number of passwords to generate.

Password Patterns
-----------------

ou can use the following characters in your pattern:

/d : Digit /c : Lowercase /C : Uppercase /e : Special characters /? :
Random characters /@ : Mixed uppercase and lowercase /& : Mixed
uppercase, lowercase, and digits

For example, the pattern [/C/c-pass-/d/?] will generate passwords with a
combination of uppercase, lowercase, digits, and random characters in
specified order.

Example
~~~~~~~

.. code:: bash

   Available Patterns:
   /d - Digit                    /c - Lowercase                
   /C - Uppercase                /e - Special characters       
   /? - Random characters        /@ - Mixed uppercase and lowercase
   /& - Mixed uppercase, lowercase, and digits

   [>] Enter pattern: /C/c/d/e/?/@/&
   [*] The maximum number of possible combinations is: 1037769600000000
   [>] Enter the number of passwords to generate (Enter for default: 1037769600000000): 100
   [>] Enter the file name (or press Enter to use passlist.txt): mypasswords.txt
   [+] Passwords generated and stored in the file 'mypasswords.txt' in 0.02 seconds.

License
-------

This project is licensed under the GNU-GPL License. See the LICENSE file
for more details.

.. |PyPI - Version| image:: https://img.shields.io/pypi/v/belch
.. |GitHub License| image:: https://img.shields.io/github/license/croketillo/belch
.. |Pepy Total Downlods| image:: https://img.shields.io/pepy/dt/belch
