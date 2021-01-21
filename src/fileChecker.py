import re

class fileChecker:
    
    def __init__(self, name):
        self.fileName = name

    def replace(self, pattern, subst): 
        self.pattern = pattern
        self.subst = subst
        # Read contents from file as a single string
        file_handle = open(self.fileName, 'r', encoding = "ISO-8859-1")
        file_string = file_handle.read()
        file_handle.close()

        # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
        file_string = (re.sub(self.pattern, self.subst, file_string))

        # Write contents to file.
        # Using mode 'w' truncates the file.
        file_handle = open(self.fileName, 'w', encoding = "ISO-8859-1")
        file_handle.write(file_string)
        file_handle.close()


