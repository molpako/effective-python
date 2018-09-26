import json
UNDEFINED = object()

# finally

handle = open('random_data.txt')
try:
    data = handle.read()
finally:
    handle.close()

# else
# どの例外が自分のコードで扱われるかわかりやすい
# try で例外が起きなければelseが実行される
def load_json_key(data, key):
    try:
        result_dict = json.loads(data)
    except ValueError as e:
        raise KeyError from e
    else:
        return result_dict[key]



def divide_json(path):
    handle = open(path, "r+")
    try:
        data = handle.read()
        op = json.loads(data)
        value = (
            op['numerator'],
            op['denominatio'])
    except ZeroDivisionError:
        return UNDEFINED
    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)
    finally:
        handle.close() 