from file_iterator.main import FileSystemIterator
from unittest import TestCase, main
from os.path import exists


path = input("Enter path to iterate from:")


class TestFSIterator(TestCase):
    def test_iterator_all(self):
        print("Testing iterations on all objects")

        for elem in FileSystemIterator(path):
            print(elem)
            self.assertTrue(exists(elem))
        print()
        print('-' * 50)

    def test_iterator_files(self):
        print("Testing iterations on files")

        for elem in FileSystemIterator(path, only_files=True):
            print(elem)
            self.assertTrue(exists(elem))
        print()
        print('-' * 50)

    def test_iterator_dirs(self):
        print("Testing iterations on directories")

        for elem in FileSystemIterator(path, only_dirs=True):
            print(elem)
            self.assertTrue(exists(elem))
        print()
        print('-' * 50)

    def test_iterator_pattern(self):
        print("Testing iterations with pattern")

        pattern = input("Enter re pattern:")
        for elem in FileSystemIterator(path, pattern=pattern):
            print(elem)
            self.assertTrue(exists(elem))
        print()
        print('-' * 50)


main()
