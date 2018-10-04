"""
C++やJavaは実行がマルチスレッドだと、CPUのマルチコアを活用できるということ
Pythonもマルチスレッド実行をサポートしているが、GIL（グローバルインタプリタロック）は
同時に1つのスレッドしか進行できないようにしている。Pythonでは複数スレッドを
使用して並列計算して速度を上げることはできないこと
"""
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

from time import time
numbers = [5354123, 2123543, 1421443, 5423123]
start = time()
for number in numbers:
    list(factorize(number))
end = time()
print('Took %.3f seconds' % (end - start)) # Took 1.176 seconds


"""
マルチスレッドで試してみる
"""
from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number
    
    def run(self):
        self.factors = list(factorize(self.number))

start = time()
threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

# すべてのスレッドが終わるのを待つ
for thread in threads:
    thread.join()

end = time()
print('Took %.3f seconds' % (end - start)) # Took 1.505 seconds


"""
遅くなった。スレッドを作成し、同期するためのオーバーヘッドのせい。
"""