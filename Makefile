PYTHON ?= python
VERSION = $(shell cat VERSION)
TAGVER = $(shell cat VERSION | sed -e "s/\([0-9\.]*\).*/\1/")

PKGNAME = mic

ifeq ($(VERSION), $(TAGVER))
	TAG = $(TAGVER)
else
	TAG = "HEAD"
endif

ifndef PREFIX
    PREFIX = "/usr/local"
endif

all:
	$(PYTHON) setup.py build

dist-bz2:
	git archive --format=tar --prefix=$(PKGNAME)-$(TAGVER)/ $(TAG) | \
		bzip2  > $(PKGNAME)-$(TAGVER).tar.bz2

dist-gz:
	git archive --format=tar --prefix=$(PKGNAME)-$(TAGVER)/ $(TAG) | \
		gzip  > $(PKGNAME)-$(TAGVER).tar.gz

install: all
	$(PYTHON) setup.py install  --prefix=$(DESTDIR)/$(PREFIX)

develop: all
	$(PYTHON) setup.py develop

clean:
	rm -f tools/*.py[co]
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/