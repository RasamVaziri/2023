Реализовать алгоритм Хаффмана. Кодирование и декодирование должно быть реализовано в одной программе. В качестве пользовательского ввода использовать аргументы командной строки, пример ввода:
./my_script --encode input_file.txt output_file.txt (сжатие)
./my_script --decode input_file.txt output_file.txt (распаковка)
В сжатый файл сначала вписывается размер словаря, затем сам словарь и после – закодированный текст. Запись в бинарном виде, так что в сжатом файле, если открыть его через обычный редактор, можно будет увидеть страшные символы (это норма).


Implement the Huffman algorithm. Encoding and decoding must be implemented in the same program. Use command line arguments as user input, input example:
./my_script --encode input_file.txt output_file.txt (compress)
./my_script --decode input_file.txt output_file.txt (decompress)
The size of the dictionary is first entered into the compressed file, then the dictionary itself, and then the encoded text. The recording is in binary form, so in a compressed file, if you open it with a regular editor, you can see scary characters (this is the norm).
