# クロージャをサポートしているので、helper()が引数のgroupにアクセスできる
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)


numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = (2, 3, 5, 7)
sort_priority(numbers, group)
print(numbers)

def sort_priotiry2(numbers, group):
    found = False
    def helper(x):
        # nonlocal文を使わないと、foundへの代入がhelper()内のスコープになる
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

# nonlocalの使用が複雑になりかけたら、ヘルパークラスでラップする
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True