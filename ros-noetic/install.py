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


# def get_missing_dependencies(pkg: str) -> list[str]:
#     depends = get_dependencies(pkg)
#     i = 0
#     while i < len(depends):
#         p = depends[i]
#         if check_installed(p):
#             depends.pop(i)
#         else:
#             for d in get_dependencies(p):
#                 if d not in depends:
#                     depends.append(d)
#             i += 1
#     return list(depends)


def install(pkg: str, asdeps: bool=False) -> None:
    if check_installed(dep):
        return

    # try this custom ros packages first
    asdep = '--asdeps' if asdeps is True else ''
    if os.path.isdir(pkg):
        print_yellow(f'INSTALLING {pkg} WITH CUSTOM PKGBUILDS')
        run(f"python install.py {asdep} {pkg}", shell=True)
        return

    # try pacman
    p = run(f"pacman -Ss '^{pkg}$'", shell=True)
    if p.returncode == 0:
        print_yellow(f'INSTALLING {pkg} WITH PACMAN')
        run(f"sudo pacman -S {asdep} {pkg}", shell=True)
        return

    # try aur
    print_yellow(f'INSTALLING {pkg} WITH YAY')
    run(f"yay --aur -S {asdep} {pkg}", shell=True)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--asdeps",
                        help="install as dependency",
                        action="store_true")
    parser.add_argument("package", help="package to install")
    args = parser.parse_args()

    deps = get_dependencies(args.package)
    print_yellow('DEPS:', deps)
    for dep in deps:
        install(dep, True)

    if check_installed(args.package) is False:
        if os.path.isdir(args.package):
            run("makepkg -i", shell=True, cwd=args.package)
