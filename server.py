from json import dumps
import logging
from os import getenv
import sys

from aiohttp import web
from atmdb import TMDbClient

logging.basicConfig(
    datefmt='%Y/%m/%d %H.%M.%S',
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

MOVIE_FIELDS = ('image_url', 'synopsis', 'title', 'url')
PERSON_FIELDS = ('biography', 'image_url', 'name', 'url')


async def random_person(_):
    """Get a random person's details."""
    logger.info('received request for random person')
    person = await tmdb_client.get_random_popular_person()
    if person is None:
        logger.warning('something went wrong')
        raise web.HTTPInternalServerError
    logger.info('retrieved information for %s', person.name)
    return web.HTTPOk(
        body=dumps(generate_payload(person)).encode('utf8'),
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


if __name__ == '__main__':
    tmdb_client = TMDbClient.from_env()
    app = web.Application()

    app.router.add_route('GET', '/api/person', random_person)

    web.run_app(app, port=getenv('PORT', 8080))
