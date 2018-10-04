"""
getやsetメソッドよりも素のままの属性を使用する
"""

"""
こうしがち
"""
class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms
    
    def get_ohms(self):
        return self._ohms
    
    def set_ohms(self, ohms):
        self._ohms = ohms
    
"""
増加演算があるときにぎこちなくなる
"""
r0 = OldResistor(50e3)
r0.set_ohms(r0.get_ohms() + 5e3)


"""
Pythonでは明示的にこのようなユーティリティメソッドは必要ない。
単純なパブリック属性で実装すべき
"""
class Resistor(object):
    def __init__(self, ohms):
        """この書き方はPython3.7から変わってる"""
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3
r1.ohms += 5e3

"""
後になって属性が設定されたときに特別に振る舞いが必要なときは
@propertyとそれに対応するsetterを舞いグレートする

voltageに値を代表することで、currentを変更できるResistorの
サブクラスを定義する。きちんとgetterとsetterの名前をプロパティ名に
合わせる。
"""
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0
    
    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


"""
voltageに代入すると、setterメソッドが実行されて対応するオブジェクトの
currentプロパティが更新される
"""
r2 = VoltageResistance(1e3)
print('Before: %5r arps' % r2.current)
r2.voltage = 10
print('After:  %5r arps' % r2.current)



"""
プロパティのsetterを指定することで、クラスに渡される値について
型や値の検査もできる。抵抗値がゼロオームより大きいことを
確かめるクラスを定義する
"""
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
    
    @property
    def ohms(self):
        return self._ohms
    
    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

r3 = BoundedResistance(1e3)
try:
    r3.ohms = 0
except Exception as e:
    print(e)
"""
ValueError: 0.000000 ohms must be > 0
"""

try:
    BoundedResistance(-5)
except Exception as e:
    print(e)
"""
ValueError: -5.000000 ohms must be > 0
"""

"""
@propertyを使って、親クラスの属性を変更不能にする。
"""
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
    
    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms
    
r4 = FixedResistance(1e3)
try:
    r4.ohms = 2e3
except Exception as e:
    print(e)

"""
@propertyで、ひどい実装をしない。たとえば、getterメソッドで
ほかの属性をセットしたりしない。
"""
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms
    
    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms

r7 = MysteriousResistor(10)
r7.current = 0.01
print('Before: %5r' % r7.voltage)
r7.ohms
print('After:  %5r' % r7.voltage)

"""
@property.setterでは関連するオブジェクト状態だけを変更すること。
オブジェクトを越えて、モジュールを動的にインポートする、遅いヘルパー関数を実行する、
高価なデータベースクエリーを行うなど呼び出し元が予期しないことをしない。
複雑だったり遅くなるようなことは通常のメソッドで行う。
"""