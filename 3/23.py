# 単純なインタフェースにはクラスの代わりに関数を使う

# フックを使用して名前のリストを長さによってソートする
names = ['Socrates', 'Archmedes', 'Plato', 'Arstotle']
names.sort(key=lambda x: len(x))
print(names)


from collections import defaultdict
def log_missing():
    print('Key added')
    return 0

current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]

result = defaultdict(log_missing, current)
print('Before:', dict(result))

for key, amount in increments:
    result[key] +=  amount
print('After: ', dict(result))

def increment_with_report(current, increments):
    added_count = 0

    def missing():
        # クロージャの状態
        nonlocal added_count
        
        added_count += 1
        return 0
    
    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount
    
    return result, added_count

result, count = increment_with_report(current, increments)
assert count == 2

class BetterCountMissing(object):
    def __init__(self):
        self.added = 0
    
    def __call__(self):
        self.added += 1
        return 0


counter = BetterCountMissing()
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount

assert counter.added == 2
