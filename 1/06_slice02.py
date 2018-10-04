x = b'sakao'
y = x[::-1]
print(y)


w = '坂尾'
x = w.encode('utf-8')
y = x[::-1]
z = y.decode('utf-8')
print(z)

"""
Traceback (most recent call last):
  File "/Users/sakaok/src/github.com/molpako/effective-python/1/slice02.py", line 9, in <module>
    z = y.decode('utf-8')
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbe in position 0: invalid start byte
"""