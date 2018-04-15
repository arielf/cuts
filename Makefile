CUTS = cuts

all:: test

test:
	(cd tests && ../runtests -c $(CUTS) tests.spec)


