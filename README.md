cuts
====

***cuts*** is Unix `cut` (and `paste`) on steroids.

`cut` is a very useful Unix utility designed to extract columns from
files.  Unfortunately, it is pretty limited in power.  In particular:

- It doesn't do automatic detection of the file input column separator
- It doesn't support mixed input separators (e.g. both CSV and TSV)
- It doesn't support multi-char column separators, in particular,
  the most common case, of any white-space sequence
- It doesn't support perl regexp separators
- It doesn't support negative (from end) column numbers
- It is non-flexible when it comes to variable number of columns in
  the input
- It is unforgiving if you accidentally use `-t` (like `sort` does) for the separator/delimiter instead of `-d` (happens to me too often)
- It generally requires too much typing for simple column extraction tasks
  and it doesn't support reasonable defaults, resulting in things like:
```
    $ cut -d, zz.csv
    cut: you must specify a list of bytes, characters, or fields
```
- It doesn't support multi-file + multi-column mixes (e.g. 2nd col
  from file1 and 3rd from file2)

Obviously with the power of the bash shell you can do stuff like:
```
    $ paste <(cut -d, -f1 file.csv) <(cut -d"\t" -f2 file.tsv)
```

but that requires too much typing (3 commands, too much shell
magic, while still not supporting regex-style separators.

Compare this to the much simpler and more intuitive `cuts` version,
which works from any shell:
```
    $ cuts file.csv 0 file.tsv 1
```

As you can see, I prefer zero-based indexing.  `cuts` uses 0 for 1st
column.

Other utilities, like `awk` give you more power at the expense of
having to learn a much more complex language to do what you want.
`cuts` is designed to give you the power you need in most cases
while always being able to stay on the command line and keeping
the human inteface _as simple as possible_

Arguments can be file-names, or column-numbers (negative offsets
from the end are supported too) or a combo of the two `file:colno`


## Reasonable defaults for everything

A file-name without a column-number will cause the last
column-number to be reused.

A column-number without a file-name will cause the last
file-name to be reused.

An undefined column-number will default to the 1st column (0)

An undefined file-name will default to `/dev/stdin`

The input column separator is the most common case of any-sequence
of white-space *or* a comma, optionally surrounded by white-space.
As a result, in 90% of cases, there's no need to specify an input
column separator.

The output column separator which is tab by default, can be
overriden using `-T <sep>` (or -S, or -D).

## Require minimal typing from the user

In addition to having reasonable defaults, `cuts` doesn't force you
to type more than needed, or enforce an order of arguments on you.
It tries to be as minimalist as possible in its requirements from the user.
Compare:

```
$ cut -d, -f 1,2,3 file.csv
```

with:

```
$ cuts file.csv 0 1 2
```


## Input flexibility and tolerance to missing data

One thing that `cuts` does is try and be completely tolerant
and supportive to cases of missing data.  If you try to paste two columns,
side-by-side, from two files but one of the files is shorter,
`cuts` will oblige and output the empty field where it is missing
from the shorter file, until it reaches EOF on the longer file.

Similarly, requesting column 2 (3rd column) when there are only
2 columns (0,1) in a line will result in an empty output for that
field rather than resulting in a fatal error.  This is done by
design and it conforms to the perl philosophy.

## A few examples
```
    cuts 0 file1 file2 file3      Extract 1st (0) column from the 3 files

    cuts file1 file2 file3 0      Same as above (order of files vs colnos doesn't matter)

    cuts file1 file2 file3        Same as above (0 is default colno)

    cuts -1 f1 f2 f3              Extract last column from each of f1, f2, and f3

    cuts file1:0 file2:-1         Extract 1st (0) column from file1 and last column from file2

    cuts 0 2 3                    Extract columns (0,2,3) from /dev/stdin

    cuts f1 0 -1 f2               Extract 1st and last columns from f1 and last column (last colno seen) from f2
```

## Usage:

Simply call `cuts` without any argument to get a full usage message:

```
$ cuts
Usage: cuts [Options] [Column_Specs]...
    Options:
        -v              verbose (mostly for debugging)

        Input column separator options (lowercase):
        -d <sep>        Use <sep> (perl regexp) as column delimiter
        -t <sep>        Alias for -d
        -s <sep>        Another alias for -d
    
        Output column separator options (uppercase of same):
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
        cuts 0 file1 file2 file3      Extract 1st (0) column from the 3 files

        cuts file1 file2 file3 0      Same as above (order of files vs colnos doesn't matter)

        cuts file1 file2 file3        Same as above (0 is default colno)

        cuts -1 f1 f2 f3              Extract last column from each of f1, f2, and f3

        cuts file1:0 file2:-1         Extract 1st (0) column from file1 and last column from file2

        cuts 0 2 3                    Extract columns (0,2,3) from /dev/stdin

        cuts f1 0 -1 f2               Extract 1st and last columns from f1 and last column (last colno seen) from f2
```

## Thoughts & TODOs (contributions welcome)

I made no effort to make `cuts` fast.  Although compared to the
I/O overhead, there may be not much need for it.  If you have ideas
on how to make the column extractions and joining more efficient,
that would be welcome.  In particular, if you extract multiple columns
from the same file, the current implementation opens it mutiple times,
just for the sake of siimplicity and generalization.  Although the
buffer cache should ensure that physical IO is avoided, having this
implemented more efficiently, would be nice.

Per file column input separators.  I haven't had the need so far so
that took a back-seat in priority.  The most common case of
intermixing TSV and CSV files as inputs is working thanks to
the current default multi-match pattern `$ICS` which simply
matching all of: multi-white-space, tabs, or space surrounded commas.
Even an extreme case of a schizophrenic input like:
```
$ cat example.csv
0,1 ,  2
0,1   ,2
0,1   ,2
a  b   c
```

Works correctly, as designed, with the present trick:
```
$ cuts -1 zz.csv
2
2
2
c
```

This is considered a blissful feature.

Implement `cut` rarely used options?  I haven't had the need for
them, and if I ever do, I can simply use `cut` itself, so I haven't
even tried to implement stuff like fixed-width field support,
byte-offsets, `--complement`, `--characters`.   The basic features
that `cut` is missing were much more critical for me when writing `cuts`.

Embed the doc in the perl executable, `perldoc` style.

Why do I support the `filename:colno` syntax? you may ask.
It seems redundant (`filename colno` would work just as well.)
The main reason is that sometimes you may have files named `1`, `2` etc.
This introduces an ambiguity: are these files or column numbers?
`cuts` solves this ambiguity by:

- Giving priority to files (it first checks arguments for file existence)
- In case you want to force `1` to a column number, even in the
  presence of a file by the same name, you can use the `file:colno` syntax.
- You may even use `;`, `#`, or `,` as the `file:colno` separator instead
  of `:` for greater control.



