import os
import sys
import shutil
from itertools import chain

from pyp2rpm_analyzer.test_set import random_packages, most_downloaded
from pyp2rpm_analyzer import settings

flags = settings.FLAGS + '  --srpm -d {}'.format(settings.SAVE_PATH)


def clean(dirname):
    """Clean content of SAVE_PATH directory."""
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    else:
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            try:
                os.remove(filepath)
            except OSError:
                shutil.rmtree(filepath)


def run_pyp2rpm(md=150, rand=150, filename=None):
    """SRPM is generated by pyp2rpm binary for each package in the set.
    Test set can be specified in file or as an number of random and
    most downloaded packages to be included.
    """
    if filename is not None:
        with open(filename, 'r') as fi:
            pkgs = fi.read().split('\n')[:-1]
    else:
        pkgs = chain(most_downloaded(md), random_packages(rand))
    # TODO warning that SAVE_PATH will be cleaned
    clean(settings.SAVE_PATH)
    failed = set()
    for pkg in pkgs:
        ret = os.system("{} {} {} {}".format(
            sys.executable, settings.PYP2RPM_BIN, flags, pkg))
        if ret != 0:
            failed.add(pkg)
    print("Failed {}".format(failed))
