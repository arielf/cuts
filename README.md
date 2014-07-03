cuts
====

***cuts***: Unix/POSIX `cut` (and `paste`) on (s)teroids.

`cut` is a very useful Unix (and POSIX standard) utility designed to
extract columns from files.  Unfortunately, it is pretty limited in power.

The following list demonstrates what is missing in `cut` and why
I felt the need to write `cuts`:

- `cut` doesn't automatically detect the file input column delimiter:
```
$ cut -f1 test.dat
0,1,2
0,1,2
0,1,2

# -- compare to cuts:
$ cuts 0 test.dat
0
0
0
```
As you can see, I prefer zero-based indexing.  `cuts` uses 0 for 1st column.

- `cut` doesn't support mixed input delimiters (e.g. both CSV and TSV)
   and it doesn't perform the commonly useful automatic side-by-side pasting:
```
#
# -- cut fails all the way on this simple example
#    Not only there's no way to mix delimiters,
#    cut doesn't do side-by-side pasting at all:
#
$ cut -d, -f2 test.csv test.tsv
1
1
1
0	1	2
0	1	2
0	1	2

#
# -- compare to cuts (auto-detect mixed delimiters & side-by-side printing):
#
$ cuts 1 test.csv test.tsv
1	1
1	1
1	1
```
- `cut` doesn't support multi-char column delimiters, in particular,
  it can't deal with the most common case of any white-space sequence
- `cut` doesn't support perl style regex delimiters, when your
  delimiter is a bit more complex (say, any sequence of non-digits)
  you're out-of-luck.
- `cut` doesn't support negative (from end) column numbers which is
  very useful when you have, say 257 fields (but you haven't counted
  them, so you don't really know), and you're interested in the last field,
  or the one before the last etc.
- `cut` doesn't support changing order of columns; it ignores the
  order requested by the user and always force-prints the fields
  in order from low to high:

```
$ cut -f3,2,1 file.tsv
0	1	2
0	1	2
0	1	2

#
# -- compare to cuts, which does exactly what you want:
#
cuts 2 1 0 file.tsv 
2	1	0
2	1	0
2	1	0
```

- `cut` is non-flexible when it comes to variable number of columns in the input
- `cut` is unforgiving if you accidentally use `-t` (like `sort` does) for the delimiter/delimiter instead of `-d` (happens to me too often)
- `cut` requires too much typing for simple column extraction tasks
  because it doesn't allow for reasonable defaults. It'll result
  in errors when arguments are missing:
```
    $ cut -d, example.csv
    cut: you must specify a list of bytes, characters, or fields

    # -- compare to cuts, where default is 1st field &
    #    field-delimiters are auto-detected for most common cases:
    $ cuts example.csv
    0
    0
    0
```
- `cut` doesn't support multi-file & multi-column mixes (e.g. 2nd col
  from file1 and 3rd from file2)

Obviously with the power of the `bash` shell you can do stuff like:
```
    $ paste <(cut -d, -f1 file.csv) <(cut -d"\t" -f2 file.tsv)
```

but that requires too much typing (3 commands & shell-magic),
while still not supporting regex-style delimiters and offsets from end.

Compare the above to the much simpler, and more intuitive, `cuts` version,
which works right out of the box, in any shell:
```
    $ cuts file.csv 0 file.tsv 1
```


Other utilities, like `awk` or `perl` give you more power at the expense
of having to learn a much more complex language to do what you want.

`cuts` is designed to give you the power you need in almost all cases,
while always being able to stay on the command line and keeping
the human interface _as simple and minimalist as possible_

`cuts` arguments can be:

    - file-names
    - column-numbers (negative offsets from the end are supported too) or
    - any combo of the two using: `file:colno`

`cuts` also supports `-` as a handy alias for `stdin`.


### Reasonable defaults for everything

A file-name without a column-number will cause the *last* specified
column-number to be reused.

A column-number without a file-name will cause the *last* specified
file-name to be reused.

An unspecified column-number will default to the 1st column (0)

An unspecified file-name will default to `/dev/stdin`so you can easily pipe
any other command output into `cuts`.

By default, the input column delimiter is the most common case of
any-sequence of white-space *or* a comma, optionally surrounded by
white-space. As a result, in the vast majority of use cases, there's
no need to specify an input column delimiter at all.  If you have
a more complex case you may overide `cuts` default
input-field-delimiter:

```
    $ cuts -d '<some-perl-regex>' ...
    # see `man perlre` for documentation on perl regular expressions
```

Similarly, the output column delimiter which is tab by default, can be
overriden using `-T <sep>` (or -S, or -D).  This is chosen
as a mnemonic: lowercase options are for input delimiters, while
the respective upper-case options are for output delimiters.

### Require minimal typing from the user

In addition to having reasonable defaults, `cuts` doesn't force you
to type more than needed, or enforce an order of arguments on you.
It tries to be as minimalist as possible in its requirements from the user.
Compare one of the simplest and most straightforward examples of
extracting 3 columns from a single file:

```
# -- the traditional cut way:
$ cut -d, -f 1,2,3 file.csv

# -- the cuts way: shorter & sweeter:
$ cuts file.csv 0 1 2
```


### Input flexibility and tolerance to missing data

One thing that `cuts` does is try and be completely tolerant
and supportive to cases of missing data.  If you try to paste two columns,
side-by-side, from two files but one of the files is shorter,
`cuts` will oblige and won't output a field where it is missing
from the shorter file, until it reaches EOF on the longer file.

Similarly, requesting column 2 (3rd column) when there are only
2 columns (0,1) in a line will result in an empty output for that
field rather than resulting in a fatal error.  This is done by
design and it conforms to the perl philosophy of silently converting
undefined values to empty ones.

### Examples

```
    cuts 0 file1 file2      Extract 1st (0) column from both files

    cuts file1 file2 0      Same as above (flexible argument order)

    cuts file1 file2        Same as above (0 is default colno)

    cuts -1 f1 f2 f3        Last column from each of f1, f2, & f3

    cuts file1:0 file2:-1   1st (0) column from file1 & last column from file2

    cuts 0 2 3              Columns (0,2,3) from /dev/stdin

    cuts f1 0 -1 f2         1st & last columns from f1
                            + last column (last colno seen) from f2

```


### Usage

Simply call `cuts` without any argument to get a full usage message:

```
$ cuts
Usage: cuts [Options] [Column_Specs]...
    Options:
        -v              verbose (mostly for debugging)

        Input column delimiter options (lowercase):
        -d <sep>        Use <sep> (perl regexp) as column delimiter
        -t <sep>        Alias for -d
        -s <sep>        Another alias for -d
    
        Output column delimiter options (uppercase of same):
        -D <sep>
        -T <sep>
        -S <sep>

    Column_Specs:
        filename:colno  Extract colno from filename
        filename        Use filename to extract columns from
        colno           Use column colno to extract columns

        If there's an excess of colno args, will duplicate the last
        file arg.  If there's an excess of file args, will duplicate
        the last colno.

        If omitted:
            Default file is /dev/stdin
            Default colno is 0

    Examples:
        cuts 0 file1 file2      1st (0) column from both files

        cuts file1 file2 0      Same as above (flexible argument order)

        cuts file1 file2        Same as above (0 is default colno)

        cuts -1 f1 f2 f3        Last column from each of f1, f2, & f3

        cuts file1:0 file2:-1   1st column from file1 & last column from file2

        cuts 0 2 3              Columns (0,2,3) from /dev/stdin

        cuts f1 0 -1 f2         1st & last columns from f1
                                + last column (last colno seen) from f2
```

### TODO items (contributions welcome)

I made no effort to make `cuts` fast.  Although compared to the
I/O overhead, there may be not much need for it.  If you have ideas
on how to make the column extractions and joining more efficient,
that would be welcome.  In particular, if you extract multiple columns
from the same file, the current implementation opens it mutiple times,
just for the sake of siimplicity and generalization.  Although the
buffer cache should ensure that physical IO is avoided, having this
implemented more efficiently, would be nice.

Per file column input delimiters.  I haven't had the need so far so
that took a back-seat in priority.  The most common case of
intermixing TSV and CSV files as inputs is working thanks to
the current default multi-match pattern `$ICS` which simply
matches all of: multi-white-space, tabs, or (optionally space surrounded)
commas.  Even an extreme case of a schizophrenic input like:

```
$ cat schizo.csv
0,1 ,  2
0,1   ,2
0,1   ,2
a  b   c
```

Works correctly, and as designed/expected, with the present smart
column-delimiter trick:

```
$ cuts -1 schizo.csv
2
2
2
c
```

I consider it a blissful feature.

Implement `cut` rarely used options?  I haven't had the need for
them, and if I ever do, I can simply use `cut` itself, so I haven't
even tried to implement stuff like fixed-width field support,
byte-offsets, `--complement`, `--characters`.   The basic features
that `cut` is missing were much more critical for me when writing `cuts`.
Still on top of this is implementing column-ranges like: 3-5 and mixed
ranges with lists like: 1,3-5,7

- Giving priority to files (it first checks arguments for file existence)
- In case you want to force `1` to a column number, even in the
  presence of a file by the same name, you can use the `file:colno` syntax.
- You may even use `#`, `,` or `;` (needs shell quoting), as the
  `file:colno` separator instead of `:` for somewhat greater control.

### Other thoughts

Why do I support the `filename:colno` syntax? you may ask.
It seems redundant (since `filename colno` works just as well.)
The reason is that sometimes you may have files named `1`, `2` etc.
This introduces an ambiguity: are these arguments files or column numbers?
`cuts` solves this ambiguity by:


