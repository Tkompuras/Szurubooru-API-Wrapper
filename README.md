# Szurubooru API Wrapper

----------

## Description

Szuwrapper is a python api wrapper designed to handle basic API calls to a Szurubooru imageboard.

## Installation
* Use pip
```bash
pip install szuwrapper
```

## Usage
* First import the Request class and create an instance of it 

```python
from szuwrapper import Request

test = Request('Username', 'Authentication_Token', 'API_URL')
```
>API_URL: If you followed the default install it should be 'http://localhost:8080/api'

* **Check the wiki for all available functions!**

## License
[MIT](https://choosealicense.com/licenses/mit/)