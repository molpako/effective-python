from urllib.parse import parse_qs

my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
print(repr(my_values))

red = my_values.get('red', [''])[0] or 0
blue = my_values.get('blue', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
print("red: {}, blue: {}, green: {}".format(red, blue, green))


def get_first_int(values, key, defalut=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])

    return defalut


red = get_first_int(my_values, 'red')
blue = get_first_int(my_values, 'blue')
green = get_first_int(my_values, 'green')
print("red: {}, blue: {}, green: {}".format(red, blue, green))
