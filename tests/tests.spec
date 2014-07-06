# This is a spec file for all tests.
# vim: textwidth=999
#
# this is a comment
#
# Test format is 2 fields, multi-space separated (3 or more spaces):
# ------------------------------------------------------------------
# the command...                                    output-reference-file
#

# simple 2 field extraction, auto comma-delimiter detect
cuts 1 2 inp/012.csv                                ref/12.tsv

# simple 2 field extraction, auto tab-delimiter detect
cuts 1 2 inp/012.tsv                                ref/12.tsv

# reverse fields
cuts 2 1 0 inp/012.tsv                              ref/210.tsv

# convert tsv to csv (all fields included)
# 3 equivalent option forms
cuts -T, 0 1 2 inp/012.tsv                          ref/012.csv
cuts -D, 0 1 2 inp/012.tsv                          ref/012.csv
cuts -S, 0 1 2 inp/012.tsv                          ref/012.csv

# mixed separators
cuts 1 inp/012.mixed	                            ref/1.tsv
cuts -1 inp/012.mixed	                            ref/2.tsv
cuts inp/012.mixed 2 1	                            ref/21.tsv

# file:colno syntax (multiple forms)
cuts inp/012.mixed:2 inp/012.tsv:1                  ref/21.tsv
cuts inp/012.mixed%2 inp/012.tsv%1                  ref/21.tsv
cuts inp/012.mixed#2 inp/012.tsv#1                  ref/21.tsv

# 3 files w/ different delimiters, same column input
cuts -1 inp/012.csv inp/012.tsv inp/012.mixed       ref/222.tsv

# schyzophrenic delimiter formats
cuts 1 inp/012.schyzo                               ref/1.tsv
cuts 0 2 2 2 inp/012.schyzo                         ref/0222.tsv

# space surrounded commas
cuts -1 -2 inp/012.cspace                           ref/21.tsv

# -- perl regexp separator: any non-digit char-sequence
cuts -t '\D+' 0 1 2 inp/012.regex                   ref/012.tsv
cuts -t '[^0-9]+' 0 1 2 inp/012.regex               ref/012.tsv

# -- excess lines
cuts -1 0 inp/012-5-lines.csv inp/012.tsv           ref/20-missing.tsv

# standard input
echo 0 1 2 3 4 5 | cuts - 1                         ref/1-1-line.tsv
echo 0 1 2 3 4 | cuts 1                             ref/1-1-line.tsv

# repeats and multies on stdin
echo 0 1 2 3 4 | cuts 1 1 0                         ref/110-1-line.tsv
cat inp/012.tsv | cuts 1 2 0                        ref/120-3-lines.tsv
cat inp/012.tsv | cuts - 1 2 0 - 2 1                ref/12021.tsv

# 1-based indexing
cuts -0 1 2 inp/012.tsv                             ref/01.tsv

# verify otions/args ambiguity separator
# (use 3 different option aliases)
cuts -d '\s+' -1 inp/012.tsv                        ref/2.tsv
cuts -s '\s+' -1 inp/012.tsv                        ref/2.tsv
cuts -t '\s+' -1 inp/012.tsv                        ref/2.tsv

# list spec expansions, incl 
cuts 1-3,2,5-7 inp/1-20-wide.csv                    ref/1-3,2,5-7.tsv
cuts ,1-3,2,5-7 inp/1-20-wide.csv                   ref/1-3,2,5-7.tsv
cuts 1-3,,,2,5,6,7 inp/1-20-wide.csv                ref/1-3,2,5-7.tsv

# list-specs w/ subset-order reversed
cuts 1-3,,2,7-5, inp/1-20-wide.csv                  ref/1-3,2,7-5.tsv
cuts 1,2,3,2,7-5 inp/1-20-wide.csv                  ref/1-3,2,7-5.tsv

# list-specs w/ mixed positive and negative offsets
cuts 2,-4--2 inp/1-20-wide.csv                      ref/2,-4--2.tsv
# same but w/ subset-order reversed
cuts 2,-2--4 inp/1-20-wide.csv                      ref/2,-2--4.tsv

# -4 .. -2
cuts 2,-4--2 inp/1-20-wide.csv                      ref/2,-4--2.tsv
# -4 .. 2 (wrap around the end, from negative to positive)
cuts 2,-4-2 inp/1-20-wide.csv                       ref/2,-4-2.tsv

# Negative direction wrap-around end
# This is actually a misfeature, it would be nicer to have this
# preserve direction, but for now it is a compromise.
cuts 2--1 inp/1-20-wide.csv                         ref/210--1.tsv


# Mixed-separator + quoted fields:
# 1) leave the quotes around the fields:
cuts -d '(?<=")[, ](?=")' 1 inp/abc.qcsv            ref/d,e,f.qsv
# 2) strip the quotes, including those at the start/end of line
#    note that the 1st quote adds a cut-point, so index is +1
cuts -d '(?:^"|"$|"[, ]")' 2 3 inp/abc.qcsv         ref/d,e,f-x,y,z.tsv


