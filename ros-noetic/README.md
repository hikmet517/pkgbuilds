# ros-noetic

- DON'T FORGET TO UPDATE `.SRCINFO` after changing ~PKGBUILD~
```fish
  makepkg --printsrcinfo > .SRCINFO
```

- cleaning
```
    # clean yay cache
    rm -rf ~/.cache/yay/....

    # pre-build packages and src, pkg
    rm -rf */src/
    rm -rf */pkg/
    rm -rf */*.pkg.tar
    rm -rf */*.pkg.tar.xz
```

- find `ros-noetic` packages
```fish
  yay -Ss ros-noetic | grep aur | sed -E 's|.+/([^ ]+) .*|\1|g' > ros-noetic-packages.txt
```

- fetch packages
```fish
  for s in (cat ros-noetic-packages.txt | string split '\n'); test -f $s.tar.gz || wget "https://aur.archlinux.org/cgit/aur.git/snapshot/$s.tar.gz"; end;
```

- untar
```fish
  for f in *.tar.gz; tar xf $f; end
```

- patch
```fish
  for f in */PKGBUILD; sed -E -i 's|^([ \t]+)(\-DCATKIN_BUILD_BINARY_PACKAGE=.+)$|\1-DCATKIN_ENABLE_TESTING=OFF \\\\\n\1\2|g' $f; end
```

- install base
```fish
  ./install.py ros-noetic-ros-core
  ./install.py ros-noetic-ros-control
  ./install.py ros-noetic-roslint
  ./install.py ros-noetic-serial
  ./install.py ros-noetic-xacro
  ./install.py ros-noetic-teleop-twist-joy
  ./install.py ros-noetic-twist-mux
  ./install.py ros-noetic-tf2-ros
  ./install.py ros-noetic-robot-localization
```

- to uninstall all ros-noetic-* packages:

```fish
  pacman -Qsq ros-noetic | sudo pacman -R -
```


# Delete all ros packages
```
  sudo pacman -R (pacman -Q | grep ros-noetic | sed -E 's|([^ ]+) .+|\1|g')
  sudo pacman -R python-catkin-tools-git
  sudo pacman -R python-catkin-tools
  sudo pacman -R python-rosdep
  sudo pacman -R python-rosdistro
  sudo pacman -R python-rospkg
  sudo pacman -R python-catkin_lint
  sudo pacman -R python-catkin_pkg
  sudo pacman -R ros-build-tools
  sudo pacman -Rns (pacman -Qtdq)
```

# clean package caches
```
    # clean yay cache
    rm -rf ~/.cache/yay/....

    # pre-build packages and src, pkg
    rm -rf */src/
    rm -rf */pkg/
    rm -rf */*.pkg.tar
    rm -rf */*.pkg.tar.xz
```
