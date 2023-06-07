


def to_snake_case(my_dict_str):
    import re
    import ast
    def convert_key(key):
        # Replace all non-alphanumeric characters with underscores
        key = re.sub(r'[^a-zA-Z0-9]', '_', key)
        # Remove any consecutive underscores
        key = re.sub(r'_+', '_', key)
        return key.lower()

    # Convert the string representation to a dictionary object
    my_dict = ast.literal_eval(my_dict_str)
    return {convert_key(key): value for key, value in my_dict.items() if value is not None}


class StringCaseConverter:
    def __init__(self, input_string: str):
        self.input_string = input_string

    def snake_to_camel(self) -> str:
        words = self.input_string.split("_")
        return words[0] + "".join(word.capitalize() for word in words[1:])

    def camel_to_snake(self) -> str:
        words = []
        word_start = 0

        for i, char in enumerate(self.input_string):
            if char.isupper():
                words.append(self.input_string[word_start:i])
                word_start = i
        words.append(self.input_string[word_start:])
        return "_".join(word.lower() for word in words)

    def sentence_to_snake(self) -> str:
        words = self.input_string.split()
        return "_".join(word.lower() for word in words)

    def sentence_to_camel(self) -> str:
        words = self.input_string.split()
        return words[0] + "".join(word.capitalize() for word in words[1:])

    def snake_or_camel_to_sentence(self) -> str:
        import re
        words = self.input_string.split("_") if "_" in self.input_string else re.findall(r"[\w']+", self.input_string)
        return " ".join(word.capitalize() for word in words)


class StringConverter:
    def __init__(self, strings):
        self.strings = strings

    def to_camel_case(self):
        return [''.join(word.capitalize() or '_' for word in string.split('_')) for string in self.strings]

    def to_snake_case(self):
        return ['_'.join(word.lower() or '_' for word in string.split(' ')) for string in self.strings]

    def to_sentence(self):
        return [' '.join(word.lower() or ' ' for word in string.split('_')) for string in self.strings]

    def from_sentence(self):
        camel_case_strings = []
        snake_case_strings = []
        for string in self.strings:
            camel_case_strings.append(''.join(word.capitalize() or '_' for word in string.split(' ')))
            snake_case_strings.append('_'.join(word.lower() or '_' for word in string.split(' ')))
        return camel_case_strings, snake_case_strings


converter = StringConverter(['hello_world', 'helloWorld', 'Hello World'])

camel_case_strings = converter.to_camel_case()  # ['helloWorld', 'helloWorld', 'HelloWorld']

snake_case_strings = converter.to_snake_case()  # ['hello_world', 'hello_world', 'hello_world']

sentence_strings = converter.to_sentence()  # ['hello world', 'hello world', 'hello world']

camel_case_strings, snake_case_strings = converter.from_sentence()  # (['HelloWorld', 'HelloWorld', 'HelloWorld'], ['hello_world', 'hello_world', 'hello_world'])

