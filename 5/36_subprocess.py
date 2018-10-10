import subprocess
proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE)
# communicate()は子プロセスの出力を読み、終了するまで待つ
out, err = proc.communicate()
print(out.decode('utf-8'))

"""
子プロセスは親プロセスのPythonインタプリタとは独立に実行される
"""
proc = subprocess.Popen(['sleep', '0.3'])
while proc.poll() is None:
    print('Working...')

def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

from time import time, sleep
start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)

for proc in procs:
    proc.communicate()
end = time()
print('Finished in %.3f ceconds' % (end - start))

def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc

import os
procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    procs.append(proc)

for proc in procs:
    out, err = proc.communicate()
    print(out[-10:])

"""
パイプみたいに子プロセスの出力をほかの入力につなげ、並列プロセスの連鎖を作れる
"""
def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5sum'],
        stdin=input_stdin,
        stdout=subprocess.PIPE
    )
    return proc

"""
一連のopensslプロセスを起動してデータを暗号化して、別のプロセス集合で
暗号化された出力をmd5でハッシュする
"""
input_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    input_procs.append(proc)
    hash_proc = run_md5(proc.stdout)
    hash_procs.append(hash_proc)

for proc in input_procs:
    proc.communicate()
for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())


"""
タイムアウト
"""
proc = run_sleep(10)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())
