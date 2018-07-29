# 悪い例
def divide1(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


# 上の悪い関数を使う場合は戻り値を評価する必要がある
result = divide1(10, 0)
if result is None:
    print('Invalide inputs')

# これは間違い
# 
x, y = 0, 5
result = divide1(x, y)
if not result:
    print('Invalid inputs')


def divide2(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

x, y = 5, 2

try:
    result = divide2(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)

# None を返すことで特別な意味を示す関数は 
# None, False, 0, "" などが全ての条件式においてFalseに評価されるのでエラーを引き押しやすい

# None の代わりに例外をあげる