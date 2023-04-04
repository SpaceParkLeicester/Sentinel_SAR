# Random Instructions

* To find all the python executables in the system, run the following
```
$ sudo find / -type f -executable -iname 'python*' -exec file -i '{}' \; | awk -F: '/x-executable; charset=binary/ {print $1}' | xargs readlink -f | sort -u | xargs -I % sh -c 'echo -n "%: "; % -V'
```