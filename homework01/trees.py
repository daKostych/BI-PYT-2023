#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 0.1

Cílem je vykreslit v "UTF16-artu" strom definovaný listem hodnot. Každý vnitřní uzel stromu obsahuje vždy dvě položky: název uzlu a seznam potomků (nemusí být nutně v tomto pořadí). Názvem může být jakýkoli objekt kromě typu list (seznam).

Příklady validních stromů:
    - triviální strom o 1 uzlu: [1, []]
    - triviální strom o 1 uzlu s opačným pořadím ID a potomků: [[], 2]
    - triviální strom o 3 uzlech: [1, [2, 3]]
        (listové uzly ve stromu o výšce >= 2 mohou být pro zjednodušení zapsány i bez prázdného seznamu potomků)

Příklady nevalidních stromů:
    - None
    - []
    - [666]
    - [1, 2]
    - (1, [2, 3])


Strom bude vykreslen podle následujících pravidel:
    - Vykresluje se shora dolů, zleva doprava.
    - Uzel je reprezentován jménem, které je stringovou serializací objektu daného v definici uzlu.
    - Uzel v hloubce N bude odsazen zlava o N×{indent} znaků, přičemž hodnota {indent} bude vždy kladné celé číslo > 1.
    - Má-li uzel K potomků, povede:
        - k 1. až K-1. uzlu šipka začínající znakem ├ (UTF16: 0x251C)
        - ke K. uzlu šipka začínající znakem └ (UTF16: 0x2514)
    - Šipka k potomku uzlu je vždy zakončena znakem > (UTF16: 0x003E; klasické "větší než").
    - Celková délka šipky (včetně úvodního znaku a koncového ">") je vždy {indent}, výplňovým znakem je zopakovaný znak ─ (UTF16: 0x2500).
    - Všichni potomci uzlu jsou spojeni na úrovni počátku šipek svislou čarou │ (UTF16: 0x2502); tedy tam, kde není jako úvodní znak ├ nebo └.
    - Pokud název uzlu obsahuje znak `\n` neodsazujte nijak zbytek názvu po tomto znaku.
    - Každý řádek je ukončen znakem `\n`.

Další požadavky na vypracovní:
    - Pro nevalidní vstup musí implementace vyhodit výjimku `raise Exception('Invalid tree')`.
    - Mít codestyle v souladu s PEP8 (můžete ignorovat požadavek na délku řádků - C0301 a používat v odůvodněných případech i jednopísmenné proměnné - C0103)
        - otestujte si pomocí `pylint --disable=C0301,C0103 trees.py`
    - Vystačit si s buildins metodami, tj. žádné importy dalších modulů.


Příklady vstupu a výstupu:
INPUT:
[[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...└──>True
│.......├──>abc
│.......└──>def
└──>2
....├──>3.14159
....└──>6.023e+23

INPUT:
[[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23, 2.718281828]], [3, ['x', 'y']], [4, []]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...├──>True
│...│...├──>abc
│...│...└──>def
│...└──>False
│.......├──>1
│.......└──>2
├──>2
│...├──>3.14159
│...├──>6.023e+23
│...└──>2.718281828
├──>3
│...├──>x
│...└──>y
└──>4

INPUT:
[6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>4
    ├>1
    │ ├>2
    │ └>3
    └>42
      ├>-43
      └>44

INPUT:
[6, [5, ['dva\nradky']]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>dva
radky

Potřebné UTF16-art znaky:
└ ├ ─ │

Odkazy:
https://en.wikipedia.org/wiki/Box_Drawing
"""


class Vertex:
    """
    Vertex class
    """
    def __init__(self):
        self.father = None
        self.sons_number = None
        self.sons_printed = 0
        self.depth = None
        self.first = False
        self.last = False
        self.value = None


def make_list(tree, vertex_list, father_index, depth, first=False, last=False):

    if not isinstance(tree, list) or len(tree) != 2:
        raise ValueError("Invalid tree")

    v = Vertex()
    v.depth = depth
    v.father = father_index
    v.first = first
    v.last = last

    sons_list = None

    if isinstance(tree[0], list):
        v.value = tree[1]
        sons_list = tree[0]
    if isinstance(tree[1], list):
        v.value = tree[0]
        sons_list = tree[1]

    if sons_list is False:
        raise ValueError('Invalid tree')

    if len(sons_list) > 2:
        v.sons_number = len(sons_list)
    elif len(sons_list) == 2 and (isinstance(sons_list[0], list) == isinstance(sons_list[1], list)):
        v.sons_number = 2
    elif len(sons_list) == 2 and (isinstance(sons_list[0], list) != isinstance(sons_list[1], list)):
        v.sons_number = 1
    elif len(sons_list) == 1:
        v.sons_number = 1
    else:
        v.sons_number = 0

    vertex_list.append(v)

    if len(sons_list) == 2 and (isinstance(sons_list[0], list)) != isinstance(sons_list[1], list):
        make_list(sons_list, vertex_list, vertex_list.index(v), depth + 1, )
    else:
        for ind, son in enumerate(sons_list):
            if isinstance(son, list):
                make_list(son, vertex_list, vertex_list.index(v), depth + 1, ind == 0, ind == len(sons_list) - 1)
            else:
                v_son = Vertex()
                v_son.depth = depth + 1
                v_son.father = vertex_list.index(v)
                v_son.sons_number = 0
                v_son.value = son
                v_son.first = ind == 0
                v_son.last = ind == len(sons_list) - 1
                vertex_list.append(v_son)

    return vertex_list


def print_tree(vertex_list, indent, separator):
    finish_string = ""
    for i in range(len(vertex_list)):

        if i == 0:
            finish_string += str(vertex_list[i].value) + '\n'
            continue

        if vertex_list[i].depth <= 2:
            if ((vertex_list[0].sons_printed == 0 and vertex_list[0].sons_number != 1) or
                    (vertex_list[0].sons_printed < vertex_list[0].sons_number - 1 and vertex_list[i].father == 0)):
                first_char = '├'
            elif vertex_list[0].sons_printed == vertex_list[0].sons_number - 1 and vertex_list[i].father == 0:
                first_char = '└'
            elif vertex_list[0].sons_printed == vertex_list[0].sons_number:
                first_char = separator
            else:
                first_char = '│'

            arrow = "├"

            if vertex_list[i].last:
                arrow = "└"

            if vertex_list[i].first:
                arrow = "├"

            if vertex_list[vertex_list[i].father].sons_number == 1:
                arrow = "└"

            if vertex_list[i].depth == 1:
                finish_string += (
                            first_char + separator * (((vertex_list[i].depth - 1) * indent) - 1) + '─' * (indent - 2)
                            + '>'
                            + str(vertex_list[i].value)
                            + '\n')
            else:
                finish_string += (first_char + separator * (((vertex_list[i].depth - 1) * indent) - 1) + arrow
                                  + '─' * (indent - 2)
                                  + '>'
                                  + str(vertex_list[i].value)
                                  + '\n')
            vertex_list[vertex_list[i].father].sons_printed += 1
        else:
            potencial_barier = []
            for j in range(i):
                if j == 0:
                    potencial_barier.append(vertex_list[j])
                    continue
                if vertex_list[j].depth < vertex_list[i].depth:
                    if vertex_list[j].depth == potencial_barier[len(potencial_barier) - 1].depth:
                        potencial_barier[len(potencial_barier) - 1] = vertex_list[j]
                    else:
                        potencial_barier.append(vertex_list[j])

            actual_barier = []
            for barier in potencial_barier:
                if barier.sons_printed == barier.sons_number:
                    actual_barier.append(False)
                else:
                    actual_barier.append(True)

            for k in range(len(actual_barier)):
                if k == 0:
                    if vertex_list[0].sons_printed == 0 or (vertex_list[0].sons_printed < vertex_list[0].sons_number - 1
                                                            and vertex_list[i].father == 0):
                        first_char = '├'
                    elif vertex_list[0].sons_printed == vertex_list[0].sons_number - 1 and vertex_list[i].father == 0:
                        first_char = '└'
                    elif vertex_list[0].sons_printed == vertex_list[0].sons_number:
                        first_char = separator
                    else:
                        first_char = '│'
                    finish_string += first_char + separator * (indent - 1)
                    continue
                if k == len(actual_barier) - 1:
                    arrow = "├"

                    if vertex_list[i].last:
                        arrow = "└"

                    if vertex_list[i].first:
                        arrow = "├"

                    if vertex_list[vertex_list[i].father].sons_number == 1:
                        arrow = "└"

                    finish_string += arrow + '─' * (indent - 2) + '>' + str(vertex_list[i].value) + '\n'
                    continue

                if actual_barier[k] is True:
                    finish_string += '│' + separator * (indent - 1)
                    continue
                if actual_barier[k] is False:
                    finish_string += separator * indent
                    continue
            vertex_list[vertex_list[i].father].sons_printed += 1

    return finish_string


# zachovejte interface metody
def render_tree(tree: list = None, indent: int = 2, separator: str = ' ') -> str:
    vertex_list = []

    make_list(tree, vertex_list, None, depth=0)

    result = print_tree(vertex_list, indent, separator)

    return result
