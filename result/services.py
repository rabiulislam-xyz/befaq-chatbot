import requests

from result.exceptions import ResultNotFoundError

API_ENDPOINT = 'https://wifaqresult.com/api/students'


def get_result_from_api(year, marhala, roll):
    try:
        url = '{}/{}/{}/{}'.format(API_ENDPOINT, year, marhala, roll)
        response = requests.get(url, timeout=10)
        result = response.json()
        if result and result.get("status") != 404:
            return result

    except Exception:
        pass

    raise ResultNotFoundError('রেজাল্ট পাওয়া যায়নি')
