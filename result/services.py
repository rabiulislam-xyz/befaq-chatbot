import requests
from bson.json_util import dumps, loads
from django.core.cache import cache
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from befaq.settings import MONGODB_URL
from result.exceptions import ResultNotFoundError

API_ENDPOINT = 'https://wifaqresult.com/api/students'


client = MongoClient(MONGODB_URL)
db = client.befaq


def insert_to_mongo(cache_key, result):
    result = dumps(result)
    try:
        db.results.insert_one({
            "cache_key": cache_key,
            "result": result
        })

    except DuplicateKeyError:
        print("duplicate error found, but result not served from mongo!")


def get_result_from_api(year, marhala, roll):
    cache_key = f"key_{year}_{marhala}_{roll}"
    print(f'made cache_key {cache_key}')

    try:
        print('try to get from cache')
        cached_result = cache.get(cache_key)
        if cached_result:
            print('result found from REDIS')
            return cached_result

        print('try to get from mongodb')
        mongo_result = db.results.find_one({"cache_key": cache_key})
        if mongo_result:
            print('result found from MONGO')
            return loads(mongo_result["result"])

        url = '{}/{}/{}/{}'.format(API_ENDPOINT, year, marhala, roll)
        print(f'requesting to api: {url}')
        response = requests.get(url, timeout=10)
        result = response.json()
        if result and result.get("status") != 404:
            print('result fetched from API')
            # set to redis cache
            cache.set(cache_key, result, timeout=600)
            # set to mongo db
            insert_to_mongo(cache_key, result)

            return result

    except Exception as e:
        print(e)

    raise ResultNotFoundError('রেজাল্ট পাওয়া যায়নি')
