
# Montreal Setup for Local Development

frontend-v2 app documentation and Dockerfile for the Montreal CKAN setup: https://hackmd.io/_m3aulK-QcKuRNAsCYMhWg

## Local CKAN backend with custom Montreal extension

CKAN 2.9.5. List of extensions for local development: `s3filestore`, `montreal`, `scheming`, `pages`, `showcase`, `harvest`, `dcat`, `spatial` and `noanonaccess`

For production `disqus` and `googleanalytics` need to be added
  

## CKAN 2.9.5 source installation

For the CKAN 2.9.5 follow the install from source installation.

http://docs.ckan.org/en/2.9/maintaining/installing/install-from-source.html


The PostgreSQL database system, v9.5 or newer. If you have a different system PostgreSQL version you can use a [dockerized postgres with pre-installed PostGIS](https://registry.hub.docker.com/r/postgis/postgis) (since postgis is needed for spatial).

If you are using dockerized postgres with postgis, the source installation is the same except the commands from step **3. Setup a PostgreSQL database** and **8.Set up the DataStore** need to be applied inside the docker container. You will also need to turn off the system's `postgresql`, which for Ubuntu you can do that with `sudo service postgresql stop`.(Example bellow with [postgis/postgis:12-3.0](https://registry.hub.docker.com/layers/postgis/postgis/postgis/12-3.0/images/sha256-71acda16357f2973034483a4a8363cc9499061120b592bcc3b7f2fbed82da621?context=explore))

```
docker pull postgis/postgis

docker run -d --name <your_container_name> -e POSTGRES_PASSWORD=<your_pass_here> -v <your_local_home_path>/postgres12-docker:/var/lib/postgresql/data -p 5432:5432 postgis/postgis:12-3.0
```
Once the container is set up continue with the source install from CKAN's documentation. For the third point **3. Setup a PostgreSQL database**, you will need to run the commands from inside of the container with the `postgres` user.
```

docker exec -it <your_container_name> bash
su postgres

```
Once inside the container and with the postgres user simply run the commands

```
psql -l
createuser -S -D -R -P ckan_default
createdb -O ckan_default ckan_default -E utf-8
```

For the seventh step in the source installation **8.Set up the DataStore**, again you will need to enter your docker container with the `postgres` user. Once inside the container run the commands to create the datastore user and datastore database.

```
createuser -S -D -R -P -l datastore_default
createdb -O ckan_default datastore_default -E utf-8
```
Setting up permissions

```
ckan -c /etc/ckan/default/ckan.ini datastore set-permissions | docker exec -i <your_container_name> psql -h localhost -p 5432 -U postgres --set ON_ERROR_STOP=1
```

There are 2 patches that do not need to be applied to CKAN for local developmemt and they can be found in the Patches folder.

## s3filestore
Follow the extension's documentation for installing it.
https://github.com/keitaroinc/ckanext-s3filestore/tree/main
For local development use [Minio](https://minio.io/). You'll need docker and docker-compose. Download the [docker-compose.yaml](https://github.com/minio/minio/blob/master/docs/orchestration/docker-compose/docker-compose.yaml?raw=true) and the [nginx.conf](https://github.com/minio/minio/blob/master/docs/orchestration/docker-compose/nginx.conf?raw=true) in your working directory. Inside the directory run:
```
docker-compose pull
docker-compose up
```
Once Minio's containers are up and running go to `localhost:9001`, enter the user and password specified in the docker-compose file and from the UI create a user identity and a bucket, then fill out the config settings.

```
ckanext.s3filestore.aws_access_key_id = <your_access_key>
ckanext.s3filestore.aws_secret_access_key = <your_secret_key>
ckanext.s3filestore.aws_bucket_name = <your_bucket_name>
ckanext.s3filestore.host_name = http://localhost:9000
ckanext.s3filestore.region_name= us-east-1
ckanext.s3filestore.signature_version = s3v4
```

## montreal
Follow the extension’s documentation for installing it.
https://github.com/VilledeMontreal/ckanext-montreal
There is a custom schema and a custom preset in this extension and once scheming is installed on your local setup you can add this to your config
```
scheming.dataset_schemas = ckanext.montreal:donneesqc_metadonnee_scheming.json
scheming.presets = ckanext.scheming:presets.json ckanext.montreal:presets.json
```

## scheming
Follow the extension’s documentation for installing it.
https://github.com/ckan/ckanext-scheming

## pages
Follow the extension’s documentation for installing it.
https://github.com/ckan/ckanext-pages/tree/v0.3.7
```
ckanext.pages.allow_html = True
ckanext.pages.editor = ckeditor
ckanext.pages.organization = True
ckanext.pages.group = True
```

## showcase
Follow the extension’s documentation for installing it.
https://github.com/ckan/ckanext-showcase/tree/v1.4.8

## harvest
Follow the extension’s documentation for installing it.
https://github.com/ckan/ckanext-harvest

## dcat
Follow the extension’s documentation for installing it.
https://github.com/ckan/ckanext-dcat

## spatial
Follow the extension’s documentation for installing it.
https://github.com/ckan/ckanext-spatial
If using the dockerized version of postgres with postgis you only need to run this commands from inside the docker container with the `postgres` user. (Example bellow with [postgis/postgis:12-3.0](https://registry.hub.docker.com/layers/postgis/postgis/postgis/12-3.0/images/sha256-71acda16357f2973034483a4a8363cc9499061120b592bcc3b7f2fbed82da621?context=explore))
```
psql -d ckan_default -f /usr/share/postgresql/12/contrib/postgis-3.0/postgis.sql
psql -d ckan_default -f /usr/share/postgresql/12/contrib/postgis-3.0/spatial_ref_sys.sql
psql -d ckan_default -c 'ALTER VIEW geometry_columns OWNER TO ckan_default;
psql -d ckan_default -c 'ALTER TABLE spatial_ref_sys OWNER TO ckan_default;
```

## noanonaccess
(not necessary for local development)
https://github.com/datopian/ckanext-noanonaccess
```
#Set this True to enable anon access for RSS feeds
ckanext.noanonaccess.allow_feeds = true
```

## Extension list in the ckan.ini
```
ckan.plugins = image_view text_view recline_view datastore datapusher s3filestore

synchronous_search stats resource_proxy recline_grid_view recline_graph_view

recline_map_view spatial_metadata spatial_query webpage_view pdf_view montreal

scheming_datasets pages showcase harvest ckan_harvester dcat dcat_rdf_harvester

dcat_json_harvester dcat_json_interface structured_data noanonaccess
```