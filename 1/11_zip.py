names = ['sakaok', 'kyouriii', 'super']
letters = [len(n) for n in names]
print(letters)

# みにくい例
longest_name = None
max_letters = 0

for i in range(len(names)):
    count = letters[i]
    if count > max_letters:
        longest_name = names[i]
        max_letters = count

print(longest_name)


for name, count in zip(names, letters):
    print(name, count)
    if count > max_letters:
        longest_name = name
        max_letters = count

