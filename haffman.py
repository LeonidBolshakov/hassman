from dataclasses import dataclass
from collections import Counter
from bisect import insort_left
from typing import Optional, Dict


@dataclass
class SymFreq:
    sym: Optional[str]      # Символ, который будет храниться (может быть None для объединенных узлов)
    freq: int               # Частота символа или сумма частот для объединенных узлов

    def __lt__(self, other):
        # Сравниваем узлы по частоте. Это нужно для правильной работы метода insort_left при вставке.
        return self.freq < other.freq

    # def __hash__(self):
    #     return hash(self.sym)


@dataclass
class Nedo:
    value: SymFreq                  # Символ и частота символа, хранящиеся в узле
    left: Optional['Nedo'] = None   # Левый ребенок (может отсутствовать)
    right: Optional['Nedo'] = None  # Правый ребенок (может отсутствовать)

    def __lt__(self, other):
        # Сравниваем узлы по частоте символов.
        # Это нужно для правильной работы метода insort_left при вставке.
        return self.value.freq < other.value.freq


def construct_sorted_frequency(input_text: str) -> [SymFreq]:
    """
    Строит список объектов SymFreq, содержащих символы входного текста и их частоты, и сортирует этот список.

    :param input_text:  Входная строка для подсчета частот символов.
    :return          :  Отсортированный список объектов SymFreq по частоте символов.
    """

    # Считаем частоты каждого символа в строке
    counter = Counter(input_text)

    # Создаем отсортированный список объектов SymFreq на основе частот
    return sorted([SymFreq(sym, freq) for sym, freq in counter.items()])


def construct_tree_haffman(sorted_frequency_: [SymFreq]) -> Nedo:
    """
     Строит дерево Хаффмана на основе отсортированного списка частот символов.

     :param sorted_frequency_: Отсортированный список частот символов.
     :return: Корневой узел построенного дерева Хаффмана
     """

    # Преобразуем объекты SymFreq в узлы Nedo
    nodes = [Nedo(sym_freq) for sym_freq in sorted_frequency_]

    # Формируем узлы дерева с суммами частот дочерних узлов до тех пор, пока не останется 1 узел
    while len(nodes) > 1:

        # Берем два узла с наименьшими частотами
        left = nodes.pop(0)
        right = nodes.pop(0)

        # Создаем новый объединенный узел с суммой частот левого и правого узлов
        merge = Nedo(SymFreq(None, left.value.freq + right.value.freq), left, right)

        # Вставляем новый узел в список в соответствующую позицию для сохранения порядка
        insort_left(nodes, merge)

    # Возвращаем корневой узел дерева, если он существует; иначе возвращаем пустой список
    return nodes[0] if len(nodes) > 0 else []


def construct_dict_haffman(root: Optional[Nedo], prefix: str = '', res: Optional[Dict[str, str]] = None) -> (
        Dict)[str, str]:
    """
    Рекурсивно строит словарь кодов Хаффмана на основе дерева Хаффмана.

    :param root: Корневой узел дерева Хаффмана.
    :param prefix: Текущий префикс (используется для формирования битового кода).
    :param res: Словарь для хранения кодов Хаффмана {символ: код}.
    :return: Словарь кодов Хаффмана {символ: код}.
    """
    if res is None:
        res = {}

    # Если дерево не исчерпано
    if root:
        # Если текущий узел является листом (символ не None), добавляем код для символа
        if root.value.sym is not None:
            res[root.value.sym] = prefix if prefix else '0'
        # Рекурсивно обрабатываем левого ребенка, добавляя '0' к префиксу
        construct_dict_haffman(root.left, prefix + '0', res)
        # Рекурсивно обрабатываем правого ребенка, добавляя '1' к префиксу
        construct_dict_haffman(root.right, prefix + '1', res)
    return res


def encoding(input_text: str, dict_haffman: dict) -> str:
    """
    Кодирование текста с помощью словаря Хаффмана.

    :param input_text:      Кодируемый текст
    :param dict_haffman:    Словарь Хаффмана
    :return:                Закодированный текст
    """

    return ''.join(dict_haffman.get(ch, '') for ch in input_text)


def decoding(input_text: str, dict_haffman: dict) -> str:
    """
    Декодирование текста, зашифрованного с помощью словаря Хаффмана
    :param input_text:      Закодированный текст
    :param dict_haffman:    Словарь Хаффмана
    :return:                Раскодированный текст
    """

    # Преобразование словаря к виду "Код: Символ".
    dict_code_ch = {code: ch for ch, code in dict_haffman.items()}

    res = ''
    code = ''
    # Поиск валидного кода во входной строке
    for ch in input_text:
        code += ch
        if code in dict_code_ch:
            res += dict_code_ch[code]
            code = ''
    if code != '':
        print(f'При декодировании символ {code}, присутствующий в коде, отсутствует в словаре Хаффмана')

    return res


def main():
    test_cases = [('beep boop beer!', 40), ('qwe5qwq', 13), ('Абракадабра', 27), ('', 0), ('fffff', 5),
                  ('Если нет хлеба, пусть едят пирожные', 146)]
    for text, expected_len in test_cases:
        sorted_frequency = construct_sorted_frequency(text)
        tree_haffman = construct_tree_haffman(sorted_frequency)
        dict_haffman = construct_dict_haffman(tree_haffman)
        code = encoding(text, dict_haffman)
        print(f'{'+ ' if text == decoding(code, dict_haffman) else '--'}'
              f'Оригинальный текст - {text:40}, Декодированный текст - {decoding(code, dict_haffman)}')


if __name__ == '__main__':
    main()
