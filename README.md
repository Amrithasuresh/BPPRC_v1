# BPPRC 2019

The pesticidal protein database is part of the Bacterial Pesticidal Protein Resource Center (BPPRC), which is under development. This database is intended to replace and extend the current [Bacillus thuringiensis nomenclature site](http://www.btnomenclature.info).

The database currently contains proteins listed in the Bt nomenclature site but with new mnemonics to reflect assignment of proteins to different homology groups. New bacteria-derived proteins with pesticidal properties are to be added.

In addition to the database, the BPPRC will contain links to additional information about these proteins, as well as applications to allow for analysis and comparison between proteins.

The development team is composed of:

Suresh Pannerselvam<sup>1</sup> ,  Neil Crickmore <sup>2</sup> ,  Colin Berry <sup>3</sup>,  Thomas Connor<sup>3</sup>, Ruchir Mishra<sup>1</sup>  and  Bryony C. Bonning<sup>1</sup>
&nbsp;
<sup>1</sup> Department of Entomology and Nematology, University of Florida, USA
<sup>2</sup> School of Life Sciences, University of Sussex, UK
<sup>3</sup> School of Biosciences, Cardiff University, UK


This is the source code of BBPRC 2019 website developed in Python/Django. To run the website locally, you need to install Django and a list of other Python packages which are listed in the requirements.txt file.


Get the development version from `Github`
--------------------------------------------

If you have `git` and `pip` installed, use this:

   pip install virtualenv
   virtualenv env
   source env/bin/activate

   git clone https://github.com/Amrithasuresh/BPPRC.git <br />
   cd bpprc <br />
   pip install -r requirements.txt <br />
   python manage.py migrate <br />
   python manage.py runserver <br />

Then copy the following URL in your browser.

http://127.0.0.1:8000/


Production installation instruction without Docker
--------------------------------------------

1.	[Celery](https://docs.celeryproject.org/en/stable/index.html) is an open-source task queue or job queue which is based on the distributed message passing. It supports scheduling too. Here we use [redis](https://redis.io/) the message-broker for celery.

*	How to install [Celery?](https://pypi.org/project/celery/)  <br />
   `pip install celery`  <br />
   
*  How to run Celery from the base project directory? Here, it will be ~/database/  Django base directory. <br />
   `celery worker -A BPPRC –loglevel=info` <br />
   
* 	How to install the Redis server? <br />
   `wget http://download.redis.io/redis-stable.tar.gz` <br />
   `tar xvzf redis-stable.tar.gz` <br />
   `cd redis-stable` <br />
   `make` <br />

* 	How to start Redis server?  <br />
   `sudo service redis start`  <br />
   
*	How to check the status of Redis server?  <br />
   `sudo service redis status`  <br />
   
2.	[PostgreSQL](https://www.postgresql.org/) is a powerful, open-source object-relational database system.

* How to install PostgreSQL? <br />
  `sudo apt-get install python-dev` <br />
  `sudo apt-get install postgresql-server-dev-9.1` <br />
  `sudo apt-get install python-psycopg2 - Or sudo pip install psycopg2` <br />
  `sudo apt-get install postgresql pgadmin3` <br />
  
* Change the default password <br />
  `sudo su` <br />
  `su postgres -c psql postgres` <br />
  `ALTER USER postgres WITH PASSWORD 'YourPassWordHere';` <br />
  `\q` <br />
 
 *	Create the database <br />
   `sudo su` <br />
   `su postgres -c psql postgres` <br />
   `CREATE DATABASE dbname;` <br />
   `CREATE USER djangouser WITH ENCRYPTED PASSWORD 'myPasswordHere';` <br />
   `GRANT ALL PRIVILEGES ON DATABASE dbname TO djangouser;` <br />
   
   
 *	Settings.py file <br />
  ` DATABASES = {` <br />
  `  'default': {` <br />
   ` 'ENGINE': 'django.db.backends.postgresql_psycopg2',` <br />
   ` 'NAME': 'dbname',` <br />
    `'USER': 'postgres',` <br />
    `'PASSWORD': 'postgres',` <br />
   ` 'HOST': '',` <br />
   ` 'PORT': '',` <br />
   ` }` <br />
  ` }` <br />
  
 
3.	Create virtual environment  <br />
   `pip install virtualenv` <br />
   `virtualenv venv` <br />
   `source venv/bin/activate` <br />
   
   * Dependencies (requirements.txt file is inside the Django base directory) <br />
   `pip install -r requirements.txt` <br />
   
4. Nginx is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache. Nginx can be deployed to server dynamic HTTP content on the network using WSGI application servers (an example) and it can serve as a software load balancer. Nginx will face the outside world. It will serve media files (images, CSS, etc) directly from the file system. However, it can't talk directly to Django applications; it needs something (uWSGI) that will run the application, feed it requests from the web, and return responses. [Source](https://serverfault.com/a/887845)

The outside world (HTTP client) <-> Nginx <-> The socket <-> uWSGI <-> Python app <br />


   * Install Nginx <br />
   `sudo apt-get install nginx ` <br />

   * Nginx configuration file Location <br />
   `/etc/nginx/conf.d/virtual.conf` <br />

   * Nginx virtual.conf file contents <br />

      `server {` <br />
        `  listen       80;` <br />
         ` server_name  {your domain_name};` <br />
         `  error_log /srv/www/database/logs/error.log;` <br />
         `  access_log /srv/www/database/logs/access.log;` <br />
          ` charset utf-8;` <br />
 
       `location /static/ {` <br />
         ` alias /srv/www/database/static/;` <br />
       `}` <br />

       `location /media/ {` <br />
         `  alias /srv/www/database/media/;` <br />
       `}` <br />

       `location / {` <br />
      	 ` add_header 'Cache-Control' 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0';` <br />
    	    ` expires off;` <br />
          ` #uwsgi_pass unix:/opt/uwsgi/sock/database.sock;` <br />
          ` proxy_connect_timeout 300s;` <br />
          ` proxy_read_timeout 300s;` <br />
          ` proxy_pass http://127.0.0.1:8000;` <br />
           `include uwsgi_params;` <br />
       `}` <br />
  
       ` #root /srv/www/database_test/database/templates/extra;` <br />
       ` #index site-down.html; ` <br />

      ` }` <br />


  * Nginx log file location <br />
    `/var/log/nginx/error.log` <br />

 






