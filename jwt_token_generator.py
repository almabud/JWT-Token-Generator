from datetime import datetime, timedelta

import jwt

jwt_token_generator = {
    'TIMEOUT': '60m',
    'ALGORITHMS': 'HS256',
    'KEY': 'almaBud'
}


class TokenGenerator:
    __timeout = None
    __algorithms = None
    __key = None
    __data = None
    __token = None

    def __init__(self, **kwargs):
        self._set_default_config()
        if not 'data' in kwargs and not 'token' in kwargs:
            raise ValueError('Missing arguments')
        if 'timeout' in kwargs:
            self.__timeout = self._get_timeout(kwargs['timeout'])
        if 'algorithms' in kwargs:
            self.__algorithms = kwargs['algorithms']
        if 'key' in kwargs:
            self.__key = kwargs['key']
        if 'data' in kwargs:
            if 'token' in kwargs:
                raise ValueError('Extra argument is given')
            self._encode_token(kwargs['data'])
        if 'token' in kwargs:
            if 'data' in kwargs or 'timeout' in kwargs:
                raise ValueError('Extra argument is given')
            self.__token = kwargs['token']

    def _set_default_config(self):
        self.__timeout = self._get_timeout(jwt_token_generator['TIMEOUT'])
        self.__key = jwt_token_generator['KEY']
        self.__algorithms = jwt_token_generator['ALGORITHMS']

    def _encode_token(self, data):
        if not isinstance(data, dict):
            raise ValueError('data must be a dict')
        data.update({'exp': self.__timeout})
        self.token = jwt.encode(data, self.__key, self.__algorithms)

    def _decode_token(self, verify):
        if not isinstance(self.__token, bytes):
            raise ValueError('token must be bytes')

        try:
            data = jwt.decode(jwt=self.__token, key=self.__key, algorithms=self.__algorithms, verify=verify)
            self.__exp = data['exp']
            del data['exp']
            self.data = data
        except Exception:
            raise Exception('Token is invalid or expired.')

    def get_exp(self):
        if not self.__token:
            raise AttributeError(f'{self.__class__} has no attribute get_exp')
        return self.__exp

    def is_valid(self, verify=True):
        if not self.__token:
            raise AttributeError(f'{self.__class__} has no attribute is_valid')
        self._decode_token(verify)
        return True
        # try:
        #     self._decode_token()
        # except Exception:
        #     return False
        # return True

    @staticmethod
    def _get_timeout(timeout):
        if not isinstance(timeout, str):
            raise ValueError('timeout must be in string')
        d = m = s = 0
        number = 0
        for item in timeout:
            if item.isdigit():
                number = number * 10 + int(item)
            if item.isalpha():
                if item == 'd':
                    d = number
                elif item == 'm':
                    m = number
                elif item == 's':
                    s = number
                else:
                    raise ValueError('Invalid timeout string')
                number = 0
        return datetime.utcnow() + timedelta(days=d, minutes=m, seconds=s)
