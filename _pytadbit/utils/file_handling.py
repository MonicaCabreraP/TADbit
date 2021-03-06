"""
22 Jan 2014
"""
from __future__ import print_function
from builtins   import next

from io       import open, TextIOWrapper, BufferedReader
import ctypes
import os
import errno
import platform

import bz2
import gzip
import zipfile
import tarfile

from subprocess import Popen, PIPE
from multiprocessing import cpu_count

try:
    basestring
except NameError:
    basestring = str


def check_pik(path):
    with open(path, "rt") as f:
        f.seek (0, 2)                # Seek @ EOF
        fsize = f.tell()             # Get Size
        f.seek (max (fsize-2, 0), 0) # Set pos @ last n chars
        key = f.read()               # Read to end
    return key == 's.'


def magic_open(filename, verbose=False, cpus=None):
    """
    To read uncompressed zip gzip bzip2 or tar.xx files

    :param filename: either a path to a file, or a file handler

    :returns: opened file ready to be iterated
    """
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

    if isinstance(filename, basestring) or isinstance(filename, basestring):
        fhandler = open(filename, 'rb')
        inputpath = True
        if tarfile.is_tarfile(filename):
            print('tar')
            thandler = tarfile.open(filename)
            if len(thandler.members) != 1:
                raise NotImplementedError(
                    'Not exactly one file in this tar archieve.')
            return magic_open(thandler.extractfile(thandler.getnames()[0]))
    else:
        fhandler = filename
        filename = fhandler.name
        inputpath = False
        start_of_file = ''
    if filename.endswith('.dsrc'):
        dsrc_binary = which('dsrc')
        if not dsrc_binary:
            raise Exception('\n\nERROR: DSRC binary not found, install it from:'
                            '\nhttps://github.com/lrog/dsrc/releases')
        proc = Popen([dsrc_binary, 'd', '-t%d' % (cpus or cpu_count()),
                      '-s', filename], stdout=PIPE, universal_newlines=True)
        return proc.stdout
    if inputpath:
        start_of_file = fhandler.read(1024)
        fhandler.seek(0)
        if is_binary_string(start_of_file):
            if start_of_file.startswith(b'\x50\x4b\x03\x04'):
                if verbose:
                    print('zip')
                zhandler = TextIOWrapper(zipfile.ZipFile(fhandler))
                if len(zhandler.NameToInfo) != 1:
                    raise NotImplementedError(
                        'Not exactly one file in this zip archieve.')
                return TextIOWrapper(BufferedReader(zhandler.open(list(zhandler.NameToInfo.keys())[0])))
            if is_binary_string(start_of_file) and start_of_file.startswith(b'\x42\x5a\x68'):
                if verbose:
                    print('bz2')
                fhandler.close()
                return TextIOWrapper(BufferedReader(bz2.BZ2File(filename)))
            if is_binary_string(start_of_file) and start_of_file.startswith(b'\x1f\x8b\x08'):
                if verbose:
                    print('gz')
                return TextIOWrapper(BufferedReader(gzip.GzipFile(fileobj=fhandler)))
        else:
            if verbose:
                print('text')
            fhandler.close()
            fhandler = open(filename, 'r')
    return fhandler


def get_free_space_mb(folder, div=2):
    """
    Return folder/drive free space (in bytes)

    Based on stackoverflow answer: http://stackoverflow.com/questions/51658/cross-platform-space-remaining-on-volume-using-python

    :param folder: folder/drive to measure
    :param 2 div: divide the size by (div*1024) to get the size in Mb (3 is Gb...)

    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/(1024**div)


def is_fastq(thing):
    """
    Check if a given file is in fastq format
    """
    if isinstance(thing, basestring):
        fh = magic_open(thing)
    else:
        fh = thing
    for _ in range(100):
        if (next(fh).startswith('@') and next(fh)[0].upper() in 'ATGCN' and
            next(fh).startswith('+') and next(fh)):
            continue
        return False
    return True


def wc(fnam):
    """
    Pythonic way to count lines
    """
    return sum(1 for _ in open(fnam,'rt'))


def mkdir(dnam):
    try:
        os.mkdir(dnam)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dnam):
            pass
        else:
            raise


def which(program):
    """
    stackoverflow: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None
