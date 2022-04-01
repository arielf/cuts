CUTS = cuts

all:: test

test:
	(cd tests && ../runtests -c $(CUTS) tests.spec)

# push to gh-pages
gh gh-pages:
	./sync-master-to-gh-pages
