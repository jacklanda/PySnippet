# -*- coding: utf-8 -*-
import os


def file_ext(filename, level=1):
    """
    return extension of filename

    Parameters:
    -----------
    filename: str
        name of file, path can be included
    level: int
        level of extension.
        for example, if filename is 'sky.png.bak', the 1st level extension
        is 'bak', and the 2nd level extension is 'png'

    Returns:
    --------
    extension of filename
    """
    return filename.split('.')[-level]


def _process_extensions(extensions=None):
    """
    preprocess and check extensions, if extensions is str, convert it to list.

    Parameters:
    -----------
    extensions: str or list/tuple of str
        file extensions

    Returns:
    --------
    extensions: list/tuple of str
        file extensions
    """
    if extensions is not None:
        if isinstance(extensions, str):
            extensions = [extensions]
        assert isinstance(extensions, (list, tuple)), \
            'extensions must be str or list/tuple of str'
        for ext in extensions:
            assert isinstance(ext, str), 'extension must be str'
    return extensions


def get_files(path, extensions=None, is_recursive=True):
    """
    Read files in path. If extensions is None, read all files, if extensions
    are specified, only read the files who have one of the extensions. If
    is_recursive is True, recursively read all files, if is_recursive is False,
    only read files in current path.

    Parameters:
    -----------
    path: str
        path to be read
    extensions: str or list/tuple of str
        file extensions
    is_recursive: bool
        whether read files recursively. read recursively is True, while just
        read files in current path if False

    Returns:
    --------
    files: A generator object which obtains all the files in path
    """
    extensions = _process_extensions(extensions)
    # get files in current path
    if not is_recursive:
        for name in os.listdir(path):
            fullname = os.path.join(path, name)
            if os.path.isfile(fullname):
                if (extensions is None) or (file_ext(fullname) in extensions):
                    yield fullname
        return files
    # get files recursively
    for main_dir, _, sub_file_list in os.walk(path):
        for filename in sub_file_list:
            fullname = os.path.join(main_dir, filename)
            if (extensions is None) or (file_ext(fullname) in extensions):
                yield fullname


if __name__ == '__main__':
    # the target path should be specified
    path = r'./output/'
    files = get_files(path)

    # merge all the .txt file in the path recursively
    with open("./merge.txt", "a+") as fw:
        for i, p in enumerate(files):
            with open(p, "r") as fr:
                content = fr.read()
                fw.write(content + "\n")
            print(f"{i+1} text files have been merged now!")
