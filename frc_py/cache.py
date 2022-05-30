from datetime import datetime, timedelta
import json
import os



class Cache:
    def __init__(self, cache_dir: str = './cache'):
        self.__cache_dir = cache_dir

    def is_cached(self, path: str, file: str) -> bool:
        return os.path.exists(os.path.join(self.__cache_dir, path, file + '.json'))

    def get(self, path: str, file: str, cache_expiry: int) -> any:
        with open(os.path.join(self.__cache_dir, path, file + '.json'), 'r', encoding='UTF-8') as f:
            data = json.load(f)
            time = datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S.%f')
            if time + timedelta(days=cache_expiry) < datetime.now():
                return None # Expired entries return None to indicate they should be refreshed
            return data['data']

    def save(self, path: str, file: str, data: any) -> None:
        if not os.path.exists(os.path.join(self.__cache_dir, path)):
            os.makedirs(os.path.join(self.__cache_dir, path))
        with open(os.path.join(self.__cache_dir, path, file + '.json'), 'w', encoding='UTF-8') as f:
            data = { 'time': datetime.utcnow().isoformat(), 'data': data }
            json.dump(data, f)
