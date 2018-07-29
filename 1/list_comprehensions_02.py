matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

flat = [x for row in matrix for x in row]
print(flat)


squared = [[x**2 for x in row] for row in matrix]
print(squared)


# これだと逆に読みにくい
my_lists = [
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [10, 11, 12]]
]

flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]

print(flat)

# ループ構造の方がいい
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)

print(flat)

# list内包表記は2つの式までに留める
