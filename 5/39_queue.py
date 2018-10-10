"""
スレッド間の協調作業にはQueueを使う

並列に動作するスレッドでは同期が必要になる。関数パイプラインを使う。
作業は各関数が次々に完了しながら、残っている関数を進行していく。
この方式はPythonで簡単に並列化できるブロッキングI/Oやサブプロセスを
含むような作業に特に適している。

例えば

1. デジタルカメラから一連の画像を取り出し
2. サイズを変更して
3. オンラインのフォトギャラリーに投稿する

というシステムを作りたいとする。
"""

# 工程をごとの関数はこれとする
def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item


"""
まず必要なのがパイプラインの段階間で作業を引き継ぐ方法。
これはスレッドセーフな生産者消費者キューでモデル化できる。
"""
from collections import deque
from threading import Lock
class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        """作業画像のリストの末尾に画像を追加する"""
        with self.lock:
            self.items.append(item)

    def get(self):
        """作業画像のリストの先頭に画像を取り出す"""
        with self.lock:
            return self.items.popleft()


"""
パイプラインの各段階を、キューから作業を取り出し関数を実行し、結果をもう一つの別のキューに置くという
Pythonスレッドとして表す
"""
from threading import Thread
from time import sleep
class Worker(Thread):
    """作業者スレッド。新しい入力のチェック数や作業量を記録する"""
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0
    
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01) # 仕事がない
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]


for thread in threads:
    thread.start()
for _ in range(1000):
    download_queue.put(object())

import time
while len(done_queue.items) < 1000:
    # Do something useful while waiting
    time.sleep(0.1)


processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print('Processed', processed, 'items after polling', polled, 'times')
"""
> Processed 1000 items after polling 3028 times

1. run()でIndexErrorをキャッチする箇所が多数回実行されている
2. 全ての入力作業完了したと決めるために、done_queueを同様にbusy waitにする必要がある
3. Workerでは、run()が永久にループしている
4. パイプラインの渋滞によって、プログラムがどこかでクラッシュすることがある。
   第1段階が早く第2段階が遅いままだと、その間のキューのサイズが増え続け第2段階が対処しきれず
   メモリを食いつぶして異常終了する

パイプラインが悪いわけではなく、優れた生産者消費者キューを作ることが難しい。
"""

