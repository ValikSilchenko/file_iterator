import re
from re import compile
from os import walk, path


class FileSystemIterator:
    def __init__(self, root: str, pattern: str = "\S*", only_files: bool = False, only_dirs: bool = False):
        try:
            assert isinstance(root, str)
            assert isinstance(pattern, str)
            assert isinstance(only_files, bool)
            assert isinstance(only_dirs, bool)
        except AssertionError:
            raise Exception("Invalid input")

        if not path.exists(root) or not path.isdir(root):
            raise Exception("Wrong path")

        self.main_iterator = walk(root)
        self.elements_iterator = iter([])

        try:
            self.compiled_pattern = re.compile(pattern)
        except re.error:
            raise Exception("Wrong regex pattern")

        self.only_files = only_files
        self.only_dirs = only_dirs
        if only_files and only_dirs:
            raise Exception("Cannot be only files and only dirs simultaneously")

        self.sys_path = root

    def __next__(self):
        while True:
            try:
                cur_elem = next(self.elements_iterator)
            except StopIteration:
                self.elements_iterator = self.get_new_elements_iterator()
                cur_elem = next(self.elements_iterator)

            if self.can_return_element(cur_elem):
                break

        return f"{self.sys_path}\\{cur_elem}"

    def __iter__(self):
        return self

    def get_new_elements_iterator(self):
        elements = []
        while not elements:
            self.sys_path, dirs, files = next(self.main_iterator)
            elements = dirs + files

        return iter(elements)

    def can_return_element(self, element):
        result = True
        if self.only_files:
            result = path.isfile(f"{self.sys_path}\\{element}")
        elif self.only_dirs:
            result = path.isdir(f"{self.sys_path}\\{element}")

        return result and self.compiled_pattern.match(element)


root_path = input("Enter path to iterate from:")

for file in FileSystemIterator(root_path, only_dirs=True):
    print(file)
