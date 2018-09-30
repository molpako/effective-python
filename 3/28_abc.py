"""
シーケンスのような単純なユースケースのクラスを設計する場合に
その要素の頻度を数える追加メソッドを持ったlistのサブクラスを直接作るとする。
"""

class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)
    
    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts

"""
listのサブクラスなのでlistの標準機能がすべて使える
"""

foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('Length is', len(foo))
foo.pop()
print('After pop', repr(foo))
print('Frequency', foo.frequency())


"""
listのサブクラスではないオブジェクトを提供する場合
"""
class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

"""
pythonはコンテナのふるまいを特殊メソッドで実装している。
bar = [1, 2, 3]
bar[0]
のようにアクセスすると
bar.__getitem__(0)
と解釈する

BinaryNodeクラスをシーケンスのようにふるまわせるには、
オブジェクトの木を深さ優先で横断する__getitem__を実装する。
"""
class IndexableNode(BinaryNode):
    def _search(self, count, index):
        found = None
        if self.left:
            found, count = self.left._search(count, index)

        if not found and count == index:
            found = self
        else:
            count += 1
        
        if not found and self.right:
            found, count = self.right._search(count, index)
        return found, count
    
    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError('Index out of range')
        return found.value

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6, right=IndexableNode(7))),
    right=IndexableNode(
        15, left=IndexableNode(11)))

print('LRR =', tree.left.right.right.value)
print('Index 0 =', tree[0])
print('Index 1 =', tree[1])
print('11 in the tree?', 11 in tree)
print('17 in the tree?', 17 in tree)
print('Tree is', list(tree))

"""
ただ、__getitem__だけでなくlen()のために__len__などの実装が必要になる
自分のコンテナ型を定義するのはかなり難しい。

Pythonでは、 collections.abcモジュールがコンテナ型の典型的なメソッドをすべて
提供する抽象基底クラスを定義している。
"""
from collections.abc import Sequence

class BadType(Sequence):
    pass

foo = BadType()
"""
Traceback (most recent call last):
  File "3/28_abc.py", line 98, in <module>
    foo = BadType()
TypeError: Can't instantiate abstract class BadType with abstract methods __getitem__, __len__
"""


"""
Python の規約に従って実装するのが必要な特殊メソッドの個数が膨大なSetやMutableMappingの
ような複雑な型でメリットが大きくなる
"""

