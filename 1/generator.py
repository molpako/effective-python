value = [len(x) for x in open('my_file.txt')]
print(value)

it = (len(x) for x in open('my_file.txt'))
print(it)

print(next(it))
print(next(it))

roots = ((x, x**0.5) for x in it)
print(roots)
print(next(roots))