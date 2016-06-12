# Known For API

Uses [aTMDb] to expose the [TMDb] API. Provides two endpoints:

 - `/api/person`: get the information for a random selection from the top 500
   most popular people on TMDb.
 - `/mock/api/person`: for easy front-end development, even offline, get the
   information for [William Fichtner][WF] (or whoever's data you place in
   `mock.json`).

Requires one environment variable to run:

  - `TMDB_API_TOKEN`: a valid token for the TMDb API.

## Deployment

### Cloud Foundry

`manifest.yml` and `runtime.txt` have been provided to make launching the API
into Cloud Foundry trivial. Simply configure the appropriate endpoint, org and
space then `cf push` from the app root to get it going.

### Docker

To help simplify client development, the API server has been set up with a
Docker container configuration. To build and run it locally:

    docker build -t <name> .
    docker run -d -e "TMDB_API_TOKEN=<your_token>" -p 8080:8080 <name>

This will spin up the API in the background and bind its port appropriately.
Take a note of the number it outputs, which is the container ID and can be used
in e.g. `docker logs` to get information on the running container.

You can use `docker-machine url` to find the address of your Docker
machine and head to `http://<docker_url>:8080/api/person` to see a random
person.

![Powered by TMDb][TMDb logo]

  [aTMDb]: https://pythonhosted.org/atmdb/
  [TMDb]: https://www.themoviedb.org/
  [TMDb logo]: https://assets.tmdb.org/images/logos/var_2_0_PoweredByTMDB_Blk_Bree.png
  [WF]: https://www.themoviedb.org/person/886