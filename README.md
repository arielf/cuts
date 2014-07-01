cuts
====

***cuts*** is Unix `cut` on steroids.

`cut` is a very useful Unix utility designed to extract columns from
files.  Unfortunately, it is very limited in power.  In particular:

- It doesn't do automatic detection of the file column separator
- It doesn't support multi-char column separators
- It doesn't support perl regexp separators
- It doesn't support negative (from end) column numbers
- It fails if you use -t (like `sort` does) for the separator/delimiter instead of -d
- It doesn't support reasonable defaults, resulting in things like:
```
    $ cut -d, zz.csv
    cut: you must specify a list of bytes, characters, or fields
```

Other utilities, like `awk` give you more power at the expense of
having to learn a much more complex language to do what you want.
`cuts` is designed to give you the power you need in ~95% of cases
while always being able to stay on the command line and keeping
the human inteface as simple as possible.

Arguments can be file-names, or column-numbers (negative offsets
from the end are supported too) or a combo of the two `file:colno`

## reasonable defaults
A file-name without a column-number will cause the last
column-number to be reused.

A column-number without a file-name will cause the last
file-name to be reused.

An undefined column-number will default to the 1st column (0)

An undefined file-name will default to /dev/stdin

The output column separator which is tab by default, can be
overriden using `-T <sep>` (or -S, or -D).

## A few examples
```
    cuts 0 file1 file2 file3      Extract 1st (0) column from the 3 files
    cuts file1 file2 file3 0      Same as above (order of files vs colnos does n't matter)

    cuts file1 file2 file3        Same as above (0 is default colno)

    cuts -1 f1 f2 f3              Extract last column from each of f1, f2, and f3

    cuts file1:0 file2:-1         Extract 1st (0) column from file1 and last column from file2

    cuts 0 2 3                    Extract columns (0,2,3) from /dev/stdin

    cuts f1 0 -1 f2               Extract 1st and last columns from f1 and last column (last colno seen) from f2
```

