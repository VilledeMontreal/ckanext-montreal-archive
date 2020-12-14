## DEPRECATED ##
See https://gitlab.com/datopian/clients/ckanext-montreal

.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org//ckanext-montreal.svg?branch=master
    :target: https://travis-ci.org//ckanext-montreal

.. image:: https://coveralls.io/repos//ckanext-montreal/badge.svg
  :target: https://coveralls.io/r//ckanext-montreal

.. image:: https://pypip.in/download/ckanext-montreal/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-montreal/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-montreal/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-montreal/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-montreal/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-montreal/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-montreal/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-montreal/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-montreal/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-montreal/
    :alt: License

=============
ckanext-montreal
=============

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!


(English version below)




------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

Pour installer ckanext-montreal:

1. Activer l'environnemnt virtuel CKAN, par exemple::

     . /usr/lib/ckan/default/bin/activate

2. Installer le package Python ckanext-montreal dans votre environnement virtuel::

     pip install ckanext-montreal

3. Ajouter ``montreal`` au paramètre ``ckan.plugins`` dans le fichier de
   configuration de CKAN (par défaut ce fichier de configuration est
   ``/etc/ckan/default/production.ini``).

4. Redémarrer CKAN. Par exemple si CKAN a été déployé avec Apache sous Ubuntu::

     sudo service apache2 reload


---------------------------
Paramètres de configuration
---------------------------


----------------------------------
Installation pour le développement
----------------------------------

Pour une installation en dev de ckanext-montreal, activer l'environnement virtuel 
de CKAN et exécuter les commandes suivantes::

    git clone https://github.com//ckanext-montreal.git
    cd ckanext-montreal
    python setup.py develop
    pip install -r dev-requirements.txt


------------------
Exécuter les tests
------------------

Exécuter les commandes suivantes pour rouler les tests::

    nosetests --nologcapture --with-pylons=test.ini

Pour rouler les tests et produire un rapport de couverture, s'assurer d'avoir
le package coverage installé dans l'environnement virtuel (``pip install coverage``)
et exécuter::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.montreal --cover-inclusive --cover-erase --cover-tests




English Version

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-montreal:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-montreal Python package into your virtual environment::

     pip install ckanext-montreal

3. Add ``montreal`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------


------------------------
Development Installation
------------------------

To install ckanext-montreal for development, activate your CKAN virtualenv and
do::

    git clone https://github.com//ckanext-montreal.git
    cd ckanext-montreal
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.montreal --cover-inclusive --cover-erase --cover-tests

