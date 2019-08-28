# To use this makefile, run the command 'make html' in the ./docs directory.

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
APIDIR        = api
BUILDDIR_API  = api/_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(APIDIR)" "$(BUILDDIR_API)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(APIDIR)" "$(BUILDDIR_API)" $(SPHINXOPTS) $(O)