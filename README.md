cuts
====

***cuts***: Unix/POSIX `cut` (and `paste`) on (s)teroids.

`cut` is a very useful Unix (and POSIX standard) utility designed to
extract columns from files.  Unfortunately, despite its usefulness
and great popularity, it is pretty limited in power.

Many <a href="http://stackoverflow.com/questions/tagged/cut">questions on stackoverflow</a>
suggest that the same pain-points of the standard `cut` are felt by many users.

The following list demonstrates what is missing in `cut` and why
I felt the need to write `cuts`:

#### `cuts` automatically detects the file input column delimiter:
```
#
# -- cut doesn't:
#
$ cut -f1 test.dat
0,1,2
0,1,2
0,1,2

#
# -- cuts does:
#
$ cuts 0 test.dat
0
0
0
```
As you can see, I prefer zero-based indexing.  `cuts` uses 0 for 1st column.

#### `cuts` supports mixed input delimiters (e.g. both CSV and TSV)
```
#
# -- cut doesn't "cut it":
#
cut -f2 t.mixed
0,1,2
0 1 2
1
#
# -- cuts does:
#
$ cuts 1 t.mixed
1
1
1
```

#### `cuts` does automatic side-by-side pasting

```
#
# -- cut doesn't output columns side-by-side when reading from
#    multiple input files, even though this is the most useful
#    and expected thing to do.
#    (It requires a separate utility like "paste")
#

#
# -- a simple example input
#
$ cat t.tsv
0	1	2
a	b	c
X	Y	Z

#
# -- cut does one file at a time:
#
$ cut -f2 t.tsv t.tsv
1
b
Y
1
b
Y

#
# -- cuts does automatic side-by-side printing:
#
$ cuts 1 t.tsv t.tsv
1	1
b	b
Y	Y
```

#### `cuts` supports multi-char column delimiters

In particular, standard `cut` can't deal with the very
common case of any white-space sequence:

```
#
# -- a file with variable length space-delimiters
#
$ cat 012.txt
0  1  2
0   1   2
0    1     2

#
# -- standard cut doesn't "cut it":
#
$ cut -d' ' -f2 012.txt



#
# -- cuts does what makes sense:
#
$ cuts 1 012.txt
1
1
1
```

#### `cuts` supports powerful (perl style) regex delimiters

When your delimiter is a bit more complex (say, any sequence of non-digits)
and you have `cut`, you're out-of-luck. `cuts` fixes this by allowing you
to specify any perl regular-expression (regexp) as the delimiter:

```
#
# -- a file with numbers separated by mixed non-numeric chars
#
$ cat 012.regex
0-----1-------2
0 ## 1 #### 2
0 aa 1 bbbbbbb 2

#
# -- cuts accepts perl regexes for delimiters
#    in this case, we set delimiter regex to any sequence of non-digits
#
$ cuts -d '[^0-9]+' 1 012.regex
1
1
1
```

#### `cuts` supports negative (from end) column numbers

This is very useful when you have, say, 257 fields (but you haven't counted
them, so you don't really know), and you're interested in the last field,
or the one before the last etc.  `cuts` supports negative offsets
from the end:

```
#
# -- Ask cuts to print last field only, by using a negative offset
#
$ cuts -1 012.txt
2
2
2

```

#### `cuts` supports changing order of columns

Unlike `cut` which ignores the order requested by the user,
and always force-prints the fields in order from low to high:

```
#
# -- cut can't change the order of columns:
#
$ cut -f3,2,1 file.tsv
0	1	2
0	1	2
0	1	2

#
# -- cuts does exactly what you ask it to:
#
$ cuts 2 1 0 file.tsv 
2	1	0
2	1	0
2	1	0
```

#### `cuts` is more powerful dealing with variable number of columns:

The ability to offset from the end of line, in combination with the
ability to specify perl regular expressions as delimiters makes some
jobs that would require writing specialized scripts,
straight-forward with `cuts`:

```
#
# -- Example file, not that Mary doesn't have a midinitial
#
$ cat t.complex
firstname  midinitial lastname    phone-number   Age
John       T.         Public      555-5555       35
Mary                  Joe         444-5555       27

#
# -- Want the phone-number? It's easy with cuts
#
$ cuts t.complex -2
phone-number
555-5555
444-5555
```

#### `cuts` is forgiving if you accidentally use `-t` (like `sort` does)

It is unfortunate that the Unix toolset is so inconsistent in the
choice of option-letters.  `cuts` solves this by allowing 'any of
the above'. So if you accidentally use `-s` instead of `-d` because
you think "separator" instead of "delimiter" - it still works
(and `-t`, which is used by `sort`, works just as well).

#### `cuts` requires minimal typing for simple column extraction tasks

`cut` is hader to use and less friendly because it doesn't support
reasonable defaults. For example:

```
#
# -- `cut` errors when arguments are missing:
#
$ cut -d, example.csv
cut: you must specify a list of bytes, characters, or fields

#
# -- compare to cuts, where default is 1st field &
#    field-delimiters are auto-detected for most common cases:
#
$ cuts example.csv
0
0
0
```

#### `cuts` supports multi-file & multi-column mixes

For example 2nd column from file1 and 3rd column from file2.

Obviously with the power of the `bash` shell you can do stuff like:
```
    $ paste <(cut -d, -f1 file.csv) <(cut -d"<TAB>" -f2 file.tsv)
```

but that requires too much typing (3 commands & shell-magic),
while still not supporting regex-style delimiters and offsets from end.

Compare the above to the much simpler, and more intuitive, `cuts` version,
which works right out of the box, in any shell:

```
$ cat file.tsv
0	1	2
a	b	c

$ cat file.csv
0,1,2
a,b,c

$ cuts file.csv 0 file.tsv 1
0	1
a	b
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


## `cuts` design principles

The following are the principles which guide the design decisions of
cuts.

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
# -- the traditional, cut way:
$ cut -d, -f 1,2,3 file.csv

# -- the cuts way: shorter & sweeter:
$ cuts file.csv 0 1 2
```

Minimal typing is also what guided the decision to include the
functionality of `paste` in `cuts`.


### Input flexibility & tolerance to missing data

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

## Examples

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


## Usage

Simply call `cuts` without any argument to get a full usage message:

```
$ cuts
Usage: cuts [Options] [Column_Specs]...
    Options:
        -v              verbose (mostly for debugging)
        -0              Don't use the default 0-based indexing, use 1-based

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
            Default colno is 0 (or 1 if 1-based indexing is in effect)

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

## Further configuration & customization

If you don't like `cuts` defaults, you can override them in
an optional personal configuration ~/.cuts.pl

If this file exists, cuts will read it during startup allowing you
override cuts default parameters, in particular the value of
the `$ICS` input-column separator regex.  The syntax of this
file is perl:

```
     # -- If you prefer 1-based indexing, by default, set this to 1
     #    You may also set it from the command-line with the
     #    -0 option.
     our $opt_0 = 0;

     # -- Alternative file:colno char separators
     our $FCsep = ':;,#';

     # -- Default input column separator (smart)
     our $ICS = '(?:\s*,\s*|\s+)';

     # -- Default output column separator
     our $OCS = "\t";

     # -- if you use a config file, you must end it with 1;
     # -- so executing it by cuts using perl 'do' succeeds.
     1;
```

## TODO items (contributions welcome)

I made no effort to make `cuts` fast.  Although compared to the
I/O overhead, there may be not much need for it.  If you have ideas
on how to make the column extractions and joining more efficient,
that would be welcome.

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

## Other thoughts

Why do I support the `filename:colno` syntax? you may ask.
It seems redundant (since `filename colno` works just as well.)
The reason is that sometimes you may have files named `1`, `2` etc.
This introduces an ambiguity: are these arguments files or column numbers?
`cuts` solves this ambiguity by:

 - Giving priority to files (it first checks arguments for file existence)
 - In case you want to force `1` to a column number, even in the
   presence of a file by the same name, you can use the `file:colno` syntax.
 - You may even use `#`, `,` or `;` (needs shell quoting), as the
  `file:colno` separator instead of `:` for somewhat greater control.


Resolving option ambiguity: negative column offsets and `-` for
`stdin` don't play well with `getopts()`.  `cuts` solves this by auto
injecting `--` (end of options marker) into `@ARGV` before calling
getopts when needed.  This is so the user never has to worry about
the ambiguity.  For example, (`-v` is `cuts` own debugging/verbose
option, while `-3` is a column index specifier) this works as expected:

```
    $ cuts -v -3 file.txt
```

