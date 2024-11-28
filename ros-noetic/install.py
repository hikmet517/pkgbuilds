#!/usr/bin/env python3

import os
from subprocess import run
import argparse


ANSI_YELLOW = '\033[1;33m'
ANSI_NORMAL = '\033[0m'
ANSI_RED = '\033[0;31m'


def print_yellow(*args):
    for arg in args:
        print(f'{ANSI_YELLOW}{arg}{ANSI_NORMAL}', end=' ')
    print()


def print_red(*args):
    for arg in args:
        print(f'{ANSI_RED}{arg}{ANSI_NORMAL}', end=' ')
    print()


def get_dependencies(pkg: str) -> list[str]:
    """Get first-level dependencies by reading .SRCINFO"""
    srcinfo_file = os.path.join(pkg, '.SRCINFO')
    if os.path.isfile(srcinfo_file) is False:
        return []
    dependencies = []
    with open(srcinfo_file) as fp:
        for line in fp:
            line = line.strip()
            if line == '':
                continue
            splitted = line.split('=')
            if len(splitted) != 2:
                continue
            k, v = [s.strip() for s in splitted]
            if k == 'depends' or k == 'makedepends':
                if v not in dependencies:
                    dependencies.append(v)
    return dependencies


def check_installed(pkg: str) -> bool:
    p = run(f'pacman -Qi "{pkg}" &>/dev/null', shell=True)
    return p.returncode == 0


def install(pkg: str, asdeps: bool=False) -> None:
    if check_installed(pkg):
        print_yellow(f'{pkg} IS ALREADY INSTALLED')
        return

    # try this custom ros packages first
    asdep = '--asdeps' if asdeps is True else ''
    if os.path.isdir(pkg):
        print_yellow(f'INSTALLING "{pkg}" WITH CUSTOM PKGBUILDS')
        run(f"python install.py {asdep} {pkg}", shell=True)
        return

    # try pacman
    p = run(f"pacman -Ss '^{pkg}$'", shell=True)
    if p.returncode == 0:
        print_yellow(f'INSTALLING "{pkg}" WITH PACMAN')
        run(f"sudo pacman -S {asdep} {pkg}", shell=True)
        return

    # try aur
    print_yellow(f'INSTALLING "{pkg}" WITH YAY')
    run(f"yay --aur -S {asdep} {pkg}", shell=True)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--asdeps",
                        help="install as dependency",
                        action="store_true")
    parser.add_argument("package", help="package to install")
    args = parser.parse_args()

    if check_installed(args.package):
        print_yellow(f'{args.package} IS ALREADY INSTALLED')
        exit(0)

    if os.path.isdir(args.package) is False:
        print_red(f'CANNOT FIND PACKAGE "{args.package}"')
        exit(1)

    deps = get_dependencies(args.package)
    print_yellow('DEPS:', deps)
    for dep in deps:
        print_yellow(f'\nINSTALLING "{dep}" AS A DEPENDENCY OF "{args.package}"')
        install(dep, True)

    run("makepkg --noconfirm --install --cleanbuild", shell=True, cwd=args.package)
