import time
from datetime import datetime

def log(message, when=datetime.now()):
    """
    関数が定義された一度だけしか評価されないため
    同じタイムスタンプが出力される
    """

    print('{}: {}'.format(when, message))

log('Hi there!')
time.sleep(0.1)
log('Hi there!')

def log_none(message, when=None):
    """Log a message with a timestamp.

    Args:
        message: Messaage to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """

    when = datetime.now() if when is None else when
    print('{}: {}'.format(when, message))

log_none('Hi there!')
time.sleep(0.1)
log_none('Hi there!')

# 引数が変更可能な場合にはNoneを使用する

import json
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)

assert foo is bar

def decode_none(data, default=None):
    """Load JSON data from a string.
    Args:
        data: JSOON data to decode.
        default: Value to return if decodeing fails.
            Defaults to an empty dictionary.
    """
    if default is None:
        default = {}
    try:
        return json.loads(data)
    except ValueError:
        return default



foo = decode_none('bad data')
foo['stuff'] = 5
bar = decode_none('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)