# @classmethodポリモルフィズムを使ってオブジェクトをジェネリックに構築する

class InputData(object):
    """入力データを表す共通クラス"""
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    """データをディスクのファイルから読み込む"""
    def __init__(self, path):
        super().__init__()
        self.path = path
    
    def read(self):
        return open(self.path).read()

class NetworkInputData(InputData):
    """ネットワークから読み込む"""
    pass



class Worker(object):
    """入力データを標準的に消費するMapReduceのWorker"""
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError
    
    def reduce(self, other):
        raise NotImplementedError

class LineCountWorker(Worker):
    """改行のカウンタを定義"""
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result

# これらの部品を、ヘルパー関数でオブジェクトを構築し連携する
import os
def generate_inputs(data_dir):
    """ディレクトリの内容をリストして
    そこに含まれる各ファイルに対するインスタンスを作る
    """
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

def create_workers(input_list):
    """generate_inputsで返されたInputDataインスタンスを
    用いてLineCountWorkerインスタンスを作る
    """
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

from threading import Thread
def execute(workers):
    """複数のスレッドに実行ステップをmapすることによって、
    これらのWorkerを並列に実行する"""
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    
    return first.result

def mapreduce(data_dir):
    """各ステップを実行する"""
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)
    


# test
from tempfile import TemporaryDirectory
import random
def write_test_files(tmpdir):
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    result = mapreduce(tmpdir)

print('There are', result, 'lines')


# mapreduce()がジェネリックではないので、@classmmethodポリモルフィズムを使う
class GenericInputData(object):
    """共通のインタフェースを用いる、新たなInputDataインスタンスを
    作る責任を負うジェネリックなクラスメソッドをもつ
    """
    def read(self):
        raise NotImplementedError
    
    @classmethod
    def generate_inputs(cls, config):
        """設定パラメータの辞書をもらう"""
        raise NotImplementedError


class PathGenericInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path
    
    def read(self):
        return open(self.path).read()
    
    @classmethod
    def generate_inputs(cls, config):
        """configで入力ファイルを探すディレクトリを指定する"""
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

class GenericWorker(object):
    """入力データを標準的に消費するMapReduceのWorker"""
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError
    
    def reduce(self, other):
        raise NotImplementedError
    
    @classmethod
    def create_workers(cls, input_class, config):
        """input_classにGenericInputDataのサブクラスを渡して、
        必要な入力を生成する。GenericWorkerの具象サブクラスのインスタンスを、
        cls()をジェネリックなコンストラクタとして呼び出し、作成する
        """
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountGenericWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def generic_mapreduce(worker_cls, input_cls, config):
    workers = worker_cls.create_workers(input_cls, config)
    return execute(workers)

with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {'data_dir': tmpdir}
    result = generic_mapreduce(LineCountGenericWorker, PathGenericInputData, config)
print('There are', result, 'lines')