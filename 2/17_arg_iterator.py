def normalize(numbers):
    """
    全体に対する割合を計算する
    """

    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80, 1000]
percentages = normalize(visits)
print(percentages)


# ジェネレータで、大きなデータセットファイルを読み込む
def read_visites(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

# イテレータが結果を一度だけしか生成しないので何も出力されたない
path = 'my_numbers.txt'
it = read_visites(path)
percentages = normalize(it)
print(percentages)

# 反復しても得られない
# StopIteration が起きないため
# 出力のないイテレータと出力を終えたイテレータかわからない
it = read_visites(path)
print(list(it))
print(list(it))


# それを解決するため、入力イテレータを最後まで動かし
# 内容全体のコピーをリストに保持する
def normalize_copy(numbers):
    numbers = list(numbers)
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


it = read_visites(path)
percentages = normalize_copy(it)
print(percentages)

# 問題点としては入力イテレータのコピーの内容次第でメモリをかなり使うこと
# 回避するために新たなイテレータを返す関数を受け入れる
def normalize_func(get_iter):
    total = sum(get_iter())
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result

# ジェネレータを呼び出して新たなイテレータをそのたび生成するlambda式を渡せる
percentages = normalize_func(lambda: read_visites(path))
print(percentages)


# lambdaを渡すのは面倒なのでイテレータプロトコルを実装した新たなコンテナクラスを提供する
class ReadVisits(object):
    def __init__(self, data_path):
        self.data_path = data_path
    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)