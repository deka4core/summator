def summator(first_number: list, second_number: list, passing=0, index=7) -> list:
    if index < 0:
        return []
    x, y, p = first_number[index], second_number[index], passing
    f = int((p and ((not x and not y) or (x and y))) or (
            not p and ((not x and y) or (x and not y))))  # МДНФ p(~x~y V xy) V ~p(~xy V x~y)
    p = int((x and y) or (x and p) or (y and p))  # МДНФ xy V xp V yp
    return summator(first_number, second_number, p, index - 1) + [f]


def number_to_decimal(number_list: list) -> int:
    output_number = 0
    is_negative = False
    length = len(number_list)
    if number_list[0] == 1:
        decrement = [1] * 8  # -1
        number_list = list(map(lambda x: int(not x), summator(number_list, decrement)))
        is_negative = True
    for i in range(length):
        output_number += 2 ** (length - (i + 1)) if number_list[i] == 1 else 0
    return -1 * output_number if is_negative else output_number
