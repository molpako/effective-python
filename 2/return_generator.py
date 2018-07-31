def index_words(text):
    """
    文字列で全ての単語の位置の添字を見つける
    """

    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)

    return result

address = 'Four score and seven years ago...'
result = index_words(address)
print(result)

# 結果リストに関する処理のすべてが取り除かれており読みやすい
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

result = list(index_words_iter(address))
print(result)
