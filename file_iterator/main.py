from re import compile
from os import walk, path


class FileSystemIterator:
    def __init__(self, root: str, pattern: str = "\S*", only_files: bool = False, only_dirs: bool = False):
        self.main_iterator = walk(root)

        self.pattern = pattern
        self.only_files = only_files
        self.only_dirs = only_dirs
        if only_files and only_dirs:
            self.only_dirs = False

        self.elements_iterator = None
        self.sys_path = root

    def __next__(self):
        if self.elements_iterator is not None:
            try:
                cur_elem = next(self.elements_iterator)
                while not (compile(self.pattern).match(cur_elem) is not None
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


root_path = input("Enter path to iterate from:")

for file in FileSystemIterator(root_path):
    print(file)
