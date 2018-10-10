"""スレッドでのデータ強豪を防ぐためにLockを使う

同じオブジェクトに複数スレッドが同時にアクセスすると危険。
例えば、センサー全体のネットワークから光のレベルのサンプルを採取するような
並列にカウントするプログラムをかく。
"""

from threading import Barrier, Thread

"""
BarrierオブジェクトはGolangでいうとこのsync.WaitGroupみたいなもん。
オブジェクトを生成するときの引数の値分、Barrier().wait()が呼び出されるまで
ブロックする機能。
"""
BARRIER = Barrier(5)

class Counter(object):
    def __init__(self):
        self.count = 0
    
    def increment(self, offset):
        self.count += offset
    
def worker(sensor_index, how_many, counter):
    BARRIER.wait()
    for _ in range(how_many):
        counter.increment(1)

def run_threads(func, how_many, counter):
    """各センサーの作業スレッドを開始し、全て読み込まれるまで待つ"""
    threads = []
    # 5つのスレッドを並列に実行する
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

how_many = 10**5
counter = Counter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))
"""
> Counter should be 500000, found 324372

結果が期待していたものと違う。
Pythonインタプリタは全てのスレッドの公平性を担保しており、それぞれがほぼ等しいプロセス時間を
得られることを保証するように実行している。そのため、Pythonは実行しているスレッドをサスペンドして
他のスレッドを順に再開させる。

相互排他ロックのLockクラスを使用する
"""


from threading import Lock
class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

counter = LockingCounter()
run_threads(worker, how_many, counter)
print('LockingCounter should be %d, found %d' % (5 * how_many, counter.count))