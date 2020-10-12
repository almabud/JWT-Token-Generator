# JWT-Token-Generator
```
jwt_token = TokenGenerator(data={'name': 'sample name'})
print(jwt_token.token)
```
##### Output:
```eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoic2FtcGxlIG5hbWUiLCJleHAiOjE2MDI1MTg0NDd9.2cLIO-CGcnqQkJILjO3p9GJOhJsidv6F38zXAZttWaw```

### Decode JWT Token:
```
token_decode = TokenGenerator(token=test_token.token)
if token_decode.is_valid():
    print(token_decode.data)
    
```
##### Output:
```
{'name': 'sample name'}
```

##### Set timeout, secret_key,  algorithms for each token:
```
token_encode = TokenGenerator(data={'name': 'sample name'}, timeout='1d 5m 7s', key='secrete_key', algorithms='HS256')
```
###### Note: d = day, m = minute, s =  second. If any parameter is 0 then just skip that parameter. eg. If day = 0d then the string look like: '5m 7s'.
##### If you set key and algorithms for each token locally then you need to pass the key and algorithms when you decode the jwt token. Other wise token invalid exception will be raised.
```
token_decode = TokenGenerator(token=test_token.token, key='secrete_key', algorithms='HS256')
if token_decode.is_valid():
    print(token_decode.data)
```
##### Output:
```
{'name': 'sample name'}
```

##### You can also set 'secrete_key', 'timeout', 'algorithms' globaly for all token. 
```
jwt_token_generator = {
    'TIMEOUT': '60m',
    'ALGORITHMS': 'HS256',
    'KEY': 'almaBud'
}
```
###### Note: Just include this to your settings file as per your settings.

