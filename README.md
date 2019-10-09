
 # BPPRC 2019

The pesticidal protein database is part of the Bacterial Pesticidal Protein Resource Center (BPPRC), which is under development. This database is intended to replace and extend the current [Bacillus thuringiensis nomenclature site](http://www.btnomenclature.info).

The database currently contains proteins listed in the Bt nomenclature site but with new mnemonics to reflect assignment of proteins to different homology groups. New bacteria-derived proteins with pesticidal properties are to be added.

In addition to the database, the BPPRC will contain links to additional information about these proteins, as well as applications to allow for analysis and comparison between proteins.

The development team is composed of:

Suresh Pannerselvam 1 ,  Neil Crickmore  2 ,  Colin Berry 3,  Thomas Connor  3, Ruchir Mishra 1  and  Bryony C. Bonning 1
1 Department of Entomology and Nematology, University of Florida, USA
2 School of Life Sciences, University of Sussex, UK
3 School of Biosciences, Cardiff University, UK


This is the source code of BBPRC 2019 website developed in Python/Django. To run the website locally, you need to install Django and a list of other Python packages which are listed in the requirements.txt file.


Get the development version from `Github`
--------------------------------------------

If you have `git` and `pip` installed, use this:

.. code-block:: bash

    git clone
    cd bbprc
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

Then copy the following URL in your browser.

.. code-block:: bash

    http://127.0.0.1:8000/
