import haffman as h

# Тесты для функции `construct_tree_haffman`


def test_construct_tree_haffman():
    # Тестовый вход
    sorted_freqs = [h.SymFreq('a', 5), h.SymFreq('b', 9), h.SymFreq('c', 12), h.SymFreq('d', 13), h.SymFreq('e', 16),
                    h.SymFreq('f', 45)]

    # Вызов функции
    tree = h.construct_tree_haffman(sorted_freqs)

    # Проверка противоположных ветвей дерева
    assert tree.left.value.freq + tree.right.value.freq == 100  # Общая частота должна быть равна 100
    assert tree.left.value.freq == 45   # Левый поддерево самое легкое (по частоте)
    assert tree.right.value.freq == 55  # Оставшаяся часть веса

    # Проверка частот и структуры дерева
    assert tree.right.left.value.freq == 25   # Проверяем вес левого узла в правом поддереве
    assert tree.right.right.value.freq == 30  # Проверяем вес правого узла в правом поддереве

    assert tree.right.left.left.value.freq == 12  # Проверяем внутренние узлы
    assert tree.right.left.right.value.freq == 13
    assert tree.right.right.left.value.freq == 14
    assert tree.right.right.right.value.freq == 16
    print("test_construct_tree_haffman пройден.")

# Тесты для функции создания словаря Хаффмана


def test_construct_dict_haffman():
    # Строим дерево
    sorted_freqs = [h.SymFreq('a', 5), h.SymFreq('b', 9), h.SymFreq('c', 12), h.SymFreq('d', 13),
                    h.SymFreq('e', 16), h.SymFreq('f', 45)]
    tree = h.construct_tree_haffman(sorted_freqs)

    # Берем ожидания по структуре дерева и строим словарь кодов Хаффмана
    huffman_dict = h.construct_dict_haffman(tree, '', {})

    # Проверка соответствия кодов
    expected_codes = {
        'a': '1100',
        'b': '1101',
        'c': '100',
        'd': '101',
        'e': '111',
        'f': '0'
    }

    for sym, code in expected_codes.items():
        assert huffman_dict[sym] == code, f"Код для {sym} неправильный: ожидал {code}, получил {huffman_dict[sym]}"
    print("test_construct_dict_haffman пройден.")

# Тесты для кодирования - раскодирования


def test_summary():
    test_cases = [('beep boop beer!', 40), ('qwe5qwq', 13), ('Абракадабра', 27), ('', 0), ('fffff', 5),
                  ('Если нет хлеба, пусть едят пирожные', 146)]
    for text, expected_len in test_cases:
        sorted_frequency = h.construct_sorted_frequency(text)
        tree_haffman = h.construct_tree_haffman(sorted_frequency)
        dict_haffman = h.construct_dict_haffman(tree_haffman)
        code = h.encoding(text, dict_haffman)

        assert len(code) == expected_len                # Контроль длины кода
        assert h.decoding(code, dict_haffman) == text   # кодированный и декодированный тексты
    print('test_summary пройден')

