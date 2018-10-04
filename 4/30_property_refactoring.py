from datetime import datetime, timedelta
class Bucket(object):
    """
    どれだけ割当量が残っており、割当量が存在する時間が
    どれだけか表す
    """
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0
    
    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota

def fill(bucket, amount):
    """バケツに水を入れるときに、前の割当量は次のピリオドを
    越えては引き継げないことを確認する"""
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    """常に使いたい量がバケツから得られるかどうかを確認する"""
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True


"""
まずはバケツに水を入れる
"""
bucket = Bucket(60)
fill(bucket, 100)
print(bucket) # Bucket(quota=100)

"""
それから、必要な割当量を引き出す
"""
if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket) # Bucket(quota=1)

"""
あるよりも多くの割当量を引き出そうとして、そこから進めなくなる
"""
if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket) # Bucket(quota=1)


"""
この実装の問題点はバケツがどれだけの割当量で始まったからわからないこと。

"""
class NewBucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0
    
    def __repr__(self):
        return 'Bucket(max_quota=%d, quota_consumed=%d)' % \
                (self.max_quota, self.quota_consumed)

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # 新たなピリオドのため、割当量をリセット
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # 新たなピリオドのため割当量を入れる
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # ピリオド内で割当量が消費される
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

bucket = NewBucket(70)
print('Initial', bucket)
fill(bucket, 100)
print('Filled', bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print('Now', bucket)

"""
あるよりも多くの割当量を引き出そうとして、そこから進めなくなる
"""
if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print('Still', bucket)

"""
Bucket.quotaを用いたコードを変更するも、クラスが変更されたことを知る必要もない。

fillとdeductをインスタンスメソッドで実装すべきかもしれないが、実際の現場では
オブジェクトがまずいインターフェースで定義されていたり、ダメなデータコンテナとして
振舞っているところから始まる場合がおおい（らしい。。。）

繰り返し@propertyを拡張する羽目になったら、クラスをリファクタリングする時期

- @propertyを使って既存のインスタンス属性に新たな機能を与える
"""

