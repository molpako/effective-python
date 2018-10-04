"""
多重継承は mix-in ユーティリティクラスだけに使う。

多重継承は避ける。多重継承による簡便さとカプセル化が望ましい場合は
代わりに mix-in を書くことを考える。

mix-in は、クラスが提供すべき一連の追加のメソッドを定義するだけの
小さなクラス。インスタンス属性も __init__ も呼び出す必要がない。
"""
 

# hasattrを用いた動的属性アクセス、isinstanceによる動的型インスペクション、
# インスタンスの辞書__dict__へのアクセスを使う。
class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)
    
    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

# このmix-inを使用して二分木の辞書表現を作るクラスの例を定義する。
class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)))

from pprint import pprint
pprint(tree.to_dict())

# BinaryTreeのサブクラスを親への参照を保持するように定義する
# この循環参照は、ToDictMixin.to_dictが無限ループしてしまう。
class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
            super().__init__(value, left=left, right=right)
            self.parent = parent
    
    # オーバライドして循環サイクルを防ぐ
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value
        return super()._traverse(key, value)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
pprint(root.to_dict())

class NamedSubTree(ToDictMixin):

    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent
    


my_tree = NamedSubTree('foobar', root.left.right)
pprint(my_tree.to_dict())
