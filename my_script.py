import sys
import argparse

import alg_haffman


def create_parser():
    """ Создаём парсер для разбора аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encode", action="store_true", default=False)
    parser.add_argument("-d", "--decode", action="store_true", default=False)
    parser.add_argument("input_file", type=argparse.FileType(encoding="utf-8"))
    parser.add_argument("output_file", type=argparse.FileType(mode="w",
            encoding="utf-8"))
    # parser.add_argument("input_file", type=argparse.FileType(encoding="1251"))
    # parser.add_argument("output_file", type=argparse.FileType(mode="w",
    #     encoding="1251"))
    # parser.add_argument("input_file", type=argparse.FileType())
    # parser.add_argument("output_file", type=argparse.FileType(mode="w"))
    return parser

def parse():
    """ Разбираем аргументы командной строки, -> command, input_file, output_file
        возвращаем команду (command = "encode"/"decode"), объекты входного 
        и выходного файлов
    """
    parser = create_parser()
    namespace = parser.parse_args()
    # если указаны оба аргумента
    if namespace.encode and namespace.decode:
        parser.error(
            "must be only one argument (-e --encode) or (-d --decode) " + \
            "you gave both")
    # если ни один не указан
    elif not (namespace.encode or namespace.decode):
        parser.error(
            "must be only one argument (-e --encode) or (-d --decode) " + \
            "there is nothing")
    command = "encode" if namespace.encode else "decode"
    input_file = namespace.input_file
    output_file = namespace.output_file
    return command, input_file, output_file

def get_substrings(string, width):
    """ "strings", 2 -> ["st", "ri", "in", "g"] """
    return [string[i:i+width] for i in range(0, len(string), width)]

def translate_bin_string_into_char_string(bin_string, width_of_slice=16):
    """ Транслирует строку из единиц и нулей в символьную, где
        width_of_slice - количество бит для конвертации в один символ.
        "1010011110..." -> "string..."
        "01" -> symbol -> "1"   # проблема перокидрования последнего символа
        ord(last_symbol) -> 2   # длина последнедней части бинарной строки
                                # служит для дополнения потерянных нулей
    """
    if not bin_string:
        raise ValueError(f"invalid bin_string: {bin_string}")
    new_string = ""
    # print("translate_bin_string_into_char_string")
    for bin_chunk in get_substrings(bin_string, width_of_slice):
        # print("bin_chunk:", bin_chunk)
        if len(bin_chunk) < width_of_slice:
            # print("bin_chunk less than width_of_slice:", bin_chunk)
            new_string += chr(int(bin_chunk.zfill(width_of_slice), base=2))
            new_string += chr(len(bin_chunk))
            break
        new_string += chr(int(bin_chunk, base=2))
    else:
        # print("append 0")
        new_string += chr(0)
    # print("new_string:", new_string)
    # print("len(new_string):", len(new_string))
    return new_string

def translate_char_string_into_bin_string(string, width_of_slice=16):
    """ Конвертируем строку из символов в строку из нулей и единиц 
        условный пример: "string" -> "01010101000110..." где width_of_slice
        - количество байтов для кодирования одного символа
        перекодирует только строку возвращённую из функции
        translate_bin_string_into_char_string(), другие строки вызовут ошибку
    """
    if len(string) < 2:
        raise ValueError(f"invalid string: \"{string}\"")
    # print("string: ", string)
    bin_string = ""
    # print("translate_char_string_into_bin_string")
    for symbol in string[:-1]:
        # "x" -> "11110000" width_of_slice=8
        bin_chunk = bin(ord(symbol))[2:]
        bin_string += bin_chunk.zfill(width_of_slice)
        # print("bin_chunk:", bin_chunk)
    else:
        bin_string = bin_string[:-width_of_slice]
        bin_string += bin_chunk.zfill(ord(string[-1]))
        # bin_chunk = bin(int(symbol.encode(encoding="1251")[0]))[2:]
        # print(f"bin_chunk: {bin_chunk}")
        # "1111" -> "00001111" width_of_slice=8
        # full_bin_chunk = bin_chunk.zfill(width_of_slice)
        # print(f"bin_chunk: {bin_chunk} full_bin_chunk: {full_bin_chunk}")
    # else:
        # последний символ хранит длину последней части бинарной строки
        # удаляем из строки последнюю часть бинарной строки, заменяем
        # на часть с нужным количеством нулей перед ней, если они "потерялись"
        # если bin_chunk = "00001111", а должен быть "001111", то будет
        # взято изначальное значение "1111" и добавлено 2 нуля
        # last_symbol = string[-1]
        # lenght_of_last_chunk = ord(last_symbol)
        # # lenght_of_last_chunk = int(last_symbol.encode(encoding="1251")[0])
        # bin_string = bin_string[:-width_of_slice]
        # last_chunk = bin_chunk.zfill(lenght_of_last_chunk)
        # bin_string += last_chunk
    return bin_string

def compress_dict(codes, width_of_slice=16):
    res_string = ""
    for key, value in codes.items():
        res = translate_bin_string_into_char_string(value, width_of_slice)
        # print(f"key: {key}, value: {value}, res: {res}")
        res_string += key + res + "::"
    else:
        res_string = res_string[:-2]
    return res_string
    # return str(codes)

def uncompress_dict(string_codes, width_of_slice=16):
    codes = {}
    for sub_string in string_codes.split("::"):
        # print("sub_string:", sub_string)
        key, chunk = sub_string[0], sub_string[1:]
        value = translate_char_string_into_bin_string(chunk, width_of_slice)
        codes[key] = value
    return codes

def main():
    command, input_file, output_file = parse()
    # width_of_slice = 14
    width_of_slice = 12
    # width_of_slice = 8
    with input_file, output_file:
        if command == "encode":
            input_text = input_file.read()
            tree = alg_haffman.get_tree(input_text)
            codes = alg_haffman.get_code(tree)
            # print(f"codes: {codes}")
            bin_string = alg_haffman.coding(input_text, codes)
            shipher_string = translate_bin_string_into_char_string(
                                bin_string, width_of_slice)
            comp_codes = compress_dict(codes, width_of_slice)
            # global global_text
            # global_text = input_text
            # global global_codes
            # global_codes = codes
            # global global_shipher_string
            # global_shipher_string = shipher_string
            # global global_bin_string
            # global_bin_string = bin_string
            # print(f"codes: {codes}")
            # print(f"shipher_string: {shipher_string}")
            output_text = comp_codes + "::::" + shipher_string
            # global global_output_text
            # global_output_text = output_text
            # output_text = shipher_string
            # output_text = output_text.encode().decode()
            output_file.write(output_text)
        elif command == "decode":
            input_text = input_file.read()
            # print(f"input_text: {input_text}")
            # print(f"input_file_text == output_file_text:", 
            #     input_text == global_output_text)
            # print("input_text.split(\"::::\")", input_text.split("::::"))
            comp_codes = input_text.split("::::")[0]
            codes = uncompress_dict(comp_codes, width_of_slice)
            shipher_string = input_text.split("::::")[1]
            # 
            # shipher_string = input_text
            # codes = global_codes
            # print(f"codes == codes_1:", global_codes == codes)
            # print(f"shipher == shipher_1:", 
            #     global_shipher_string == shipher_string)
            # print(f"codes: {codes}")
            # print(f"shipher_string: {shipher_string}")
            bin_string = translate_char_string_into_bin_string(
                            shipher_string, width_of_slice)
            # print(f"bin_string == bin_string_1:", bin_string == global_bin_string)
            # print(f"bin_string: {bin_string}")
            output_text = alg_haffman.decoding(bin_string, codes)
            # output_text = output_text.encode().decode()
            output_file.write(output_text)
            # global global_text
            # print(f"text == text_1:", output_text == global_text)

def testing_cli():
    # sys.argv = [__name__, "--encode"]
    # sys.argv = [__name__, "--encode", "-d"]
    # sys.argv = [__name__]
    # sys.argv = [__name__, "--encode", "input_file.txt"]
    sys.argv = [__name__, "--encode", "input_file.txt", "output_file.txt"]
    sys.argv = [__name__, "--decode", "input_file.txt", "output_file.txt"]
    command, input_file, output_file = parse()
    print(f"command: {command}, input_file: {input_file}," + \
        f" output_file {output_file}")
    print("read: ", input_file.read())
    print("write: ", output_file.write("Hello"))

def testing_translation_bin_in_str():
    strings = (
        "А",
        "мама",
        "маленькая строка",
        "строка чуть по-больше",
        "english кириллица",
        "знаки припинания .,!",
    )
    print("testing_translation_bin_in_str")
    for string in strings:
        tree = alg_haffman.get_tree(string)
        codes = alg_haffman.get_code(tree)
        bin_string = alg_haffman.coding(string, codes)
        # print(f"string: {string}")
        shipher_string = translate_bin_string_into_char_string(bin_string, 8)
        bin_string_1 = translate_char_string_into_bin_string(shipher_string, 8)
        print(string, bin_string == bin_string_1)

def testing_compress_uncompres_dict():
    strings = (
        "1",
        "12",
        "123",
        "12345",
        "string",
        "кириллица",
        "english и кириллица",
        "знаки припинания .,!2№",
        "".join([chr(i) for i in range(1000)]),

    )
    print("testing_compress_uncompres_dict")
    for string in strings:
        tree = alg_haffman.get_tree(string)
        codes = alg_haffman.get_code(tree)
        comp_codes = compress_dict(codes)
        codes_1 = uncompress_dict(comp_codes)
        print(f"string: {string}, {codes == codes_1}")
    pass

def testing_file_read_write():
    sys.argv = [__name__, "--encode", "input_file.txt", "output_file.txt"]
    command, input_file, output_file = parse()
    with input_file, output_file:
        print("input_file.read():", input_file.read())
        print("output_file.write():", output_file.write("hello"))
    print("input_file.closed:", input_file.closed)
    # print("output_file.closed:", output_file.closed)

def testing_program():
    print("testing encoding file")
    sys.argv = [__name__, "--encode", "input_file.txt", "output_file.txt"]
    main()
    print("done testing encoding file")
    print("testing decoding file")
    sys.argv = [__name__, "--decode", "output_file.txt", "new_file.txt"]
    main()
    print("done testing decoding file")

def testing_get_substrings():
    print("testing_get_substrings")
    string = "string"
    for i in range(1, 10):
        res = get_substrings(string, i)
        print(res, i, len(res) == len(string) // i + bool(len(string) % i))


if __name__ == '__main__':
    # testing_cli()
    # testing_translation_bin_in_str()
    # testing_compress_uncompres_dict()
    # testing_get_substrings()
    # testing_file_read_write()
    # testing_program()
    main()

    # string = "string"
    # tree = alg_haffman.get_tree(string)
    # codes = alg_haffman.get_code(tree)
    # bin_string = alg_haffman.coding(string, codes)
    # shipher_string = translate_bin_string_into_char_string(bin_string)
    # bin_string_1 = translate_char_string_into_bin_string(shipher_string)
    # string_1 = alg_haffman.decoding(bin_string_1, codes)
    # print(string == string_1)
    # print(f"string: {string}")
    # print(f"string_1: {string_1}")
    # print(f"bin_string: {bin_string}")
    # print(f"shipher_string: {shipher_string}")
    pass
