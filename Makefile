
BINDIR = /usr/local/bin

INSTALL = install

install:
	$(INSTALL) -m 755 xml2flat.py $(BINDIR)/xml2flat

uninstall:
	rm $(BINDIR)/xml2flat
