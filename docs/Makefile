SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile deploy

deploy: html
	@set -e; \
	repo=$$(git rev-parse --show-toplevel); \
	url=$$(git -C "$$repo" remote get-url origin); \
	tmp=$$(mktemp -d); \
	cp -a $(BUILDDIR)/html/. "$$tmp"/; \
	touch "$$tmp/.nojekyll"; \
	git -C "$$tmp" init -q; \
	git -C "$$tmp" checkout -q --orphan gh-pages; \
	git -C "$$tmp" add -A; \
	git -C "$$tmp" -c user.name="docs bot" -c user.email="docs@localhost" \
	    commit -qm "Deploy docs $$(date -u +%Y-%m-%dT%H:%M:%SZ)"; \
	git -C "$$tmp" remote add origin "$$url"; \
	git -C "$$tmp" push -f origin gh-pages; \
	rm -rf "$$tmp"

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
