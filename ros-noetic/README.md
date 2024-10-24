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
```

- to uninstall all ros-noetic-* packages:

```fish
  pacman -Qsq ros-noetic | pacman -R -
```
