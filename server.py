from json import dumps
import logging
from os import getenv
import sys

from aiohttp import web
from aiohttp_cors import setup, ResourceOptions
from atmdb import TMDbClient

logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

MOVIE_FIELDS = ('image_url', 'release_year', 'synopsis', 'title', 'url')
PERSON_FIELDS = ('age', 'biography', 'image_url', 'name', 'url')

with open('mock.json') as mock_data:
    MOCK_DATA = mock_data.read()

with open('search.json') as mock_data:
    MOCK_SEARCH = mock_data.read()


async def random_person(_):
    """Get a random person's details."""
    logger.info('received request for random person')
    person = await tmdb_client.get_random_popular_person()
    if person is None:
        logger.warning('something went wrong')
        raise web.HTTPInternalServerError
    logger.info('retrieved information for %s', person.name)
    return create_response(generate_payload(person))


async def search(req):
    """Search for a movie title."""
    query = req.GET['query']
    logger.info('received request to search for "{}"'.format(query))
    movies = await tmdb_client.find_movie(query)
    return create_response([movie.title for movie in movies[:5] or []])


async def mock_random_person(_):
    """Mock endpoint for testing."""
    return web.HTTPOk(
        body=MOCK_DATA.encode('utf8'),
        content_type='application/json',
    )


async def mock_search(req):
    """Mock endpoint for testing."""
    _ = req.GET['query']
    return web.HTTPOk(
        body=MOCK_SEARCH.encode('utf8'),
        content_type='application/json',
    )


async def config(_):
    """Return the current client config."""
    updated = tmdb_client.config.get('last_update')
    return create_response(dict(
        data=tmdb_client.config.get('data'),
        last_update=format_datetime(updated),
    ))


def create_response(body):
    """Return 200 OK with JSON."""
    return web.HTTPOk(
        body=dumps(body).encode('utf8'),
        content_type='application/json',
    )


def generate_payload(person):
    """Convert Person object to JSON payload."""
    payload = {attr: getattr(person, attr) for attr in PERSON_FIELDS}
    payload.update(known_for=[
        {attr: getattr(movie, attr) for attr in MOVIE_FIELDS}
        for movie in person.known_for
        ])
    return payload


def format_datetime(datetime_):
    """Convert datetime object to something JSON-serializable."""
    if datetime_ is None:
        return None
    return datetime_.strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == '__main__':
    tmdb_client = TMDbClient.from_env()
    app = web.Application()
    cors = setup(app, defaults={
        'http://known-for-web.cfapps.pez.pivotal.io': ResourceOptions(),
    })

    for route, func in [
        ('/api/person', random_person),
        ('/api/search', search),
        ('/mock/api/person', mock_random_person),
        ('/mock/api/search', mock_search),
        ('/api/config', config),
    ]:
        route = cors.add(app.router.add_route('GET', route, func))

    web.run_app(app, port=getenv('PORT', 8080))
