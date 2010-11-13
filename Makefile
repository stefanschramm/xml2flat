PREFIX = /usr
BINDIR = $(PREFIX)/bin
MANDIR = $(PREFIX)/share/man/man1

INSTALL = install
GROFF = groff

all:	README

install:
	$(INSTALL) -m 755 xml2flat.py $(BINDIR)/xml2flat
	$(INSTALL) -m 644 doc/xml2flat.1 $(MANDIR)/xml2flat.1

uninstall:
	rm $(BINDIR)/xml2flat
	rm $(MANDIR)/xml2flat.1

README:
	# readme is the manpage
	$(GROFF) -man -Tascii doc/xml2flat.1 > README
