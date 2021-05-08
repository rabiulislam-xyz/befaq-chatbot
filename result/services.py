import requests
from django.core.cache import cache

from result.exceptions import ResultNotFoundError

API_ENDPOINT = 'https://wifaqresult.com/api/students'


def get_result_from_api(year, marhala, roll):
    try:
        # try to get from cache
        cached_result = cache.get(f"{year}_{marhala}_{roll}")
        if cached_result:
            return cached_result

        url = '{}/{}/{}/{}'.format(API_ENDPOINT, year, marhala, roll)
        response = requests.get(url, timeout=10)
        result = response.json()
        if result and result.get("status") != 404:
            # set cache
            cache.set(f"{year}_{marhala}_{roll}", result, timeout=None)
            return result

    except Exception as e:
        print(e)

    raise ResultNotFoundError('রেজাল্ট পাওয়া যায়নি')
