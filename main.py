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

        try:
            self.compiled_pattern = re.compile(pattern)
        except re.error:
            raise Exception("Wrong regex pattern")

        self.only_files = only_files
        self.only_dirs = only_dirs
        if only_files and only_dirs:
            raise Exception("Cannot be only files and only dirs simultaneously")

        self.elements_iterator = None
        self.sys_path = root

    def __next__(self):
        if self.elements_iterator is not None:
            try:
                cur_elem = next(self.elements_iterator)
                while not (self.compiled_pattern.match(cur_elem) is not None
                           and (self.only_files and path.isfile(f"{self.sys_path}\\{cur_elem}")
                                or self.only_dirs and path.isdir(f"{self.sys_path}\\{cur_elem}")
                                or not (self.only_files or self.only_dirs))):
                    cur_elem = next(self.elements_iterator)
                return f"{self.sys_path}\\{cur_elem}"
            except StopIteration:
                pass
        self.sys_path, dirs, files = next(self.main_iterator)
        self.elements_iterator = (elem for elem in dirs + files)  # creating generator from lists

        return next(self)

    def __iter__(self):
        return self


# root_path = input("Enter path to iterate from:")
root_path = "C:/pb/src"

for file in FileSystemIterator(root_path):
    print(file)
