import re


class FileChecker:

    def __init__(self, name):
        self.fileName = name

    def replace(self, pattern, subst):
        # Wczytuje zawartość pliku jako pojedynczy ciąg
        file_handle = open(self.fileName, 'r', encoding="ISO-8859-1")
        file_string = file_handle.read()
        file_handle.close()

        # Przy pomocy pakietu RE można zastąpić określone części stringa
        file_string = (re.sub(pattern, subst, file_string))

        # Zapis zawartości do pliku z nadpisywaniem
        file_handle = open(self.fileName, 'w', encoding="ISO-8859-1")
        file_handle.write(file_string)
        file_handle.close()
