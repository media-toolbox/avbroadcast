# ------
# Common
# ------

$(eval venvpath     := .venv_util)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval bumpversion  := $(venvpath)/bin/bumpversion)
$(eval twine        := $(venvpath)/bin/twine)
$(eval sphinx       := $(venvpath)/bin/sphinx-build)

setup-virtualenv:
	@test -e $(python) || `command -v virtualenv` --python=`command -v python` --no-site-packages $(venvpath)


# -------
# Release
# -------

setup-release: setup-virtualenv
	$(pip) install --quiet --requirement requirements-release.txt

bumpversion:
	$(bumpversion) $(bump)

push:
	git push && git push --tags

sdist:
	$(python) setup.py sdist

upload:
	$(twine) upload --skip-existing dist/*.tar.gz

# make release bump=minor  (major,minor,patch)
release: setup-release bumpversion push sdist upload


# -------------
# Documentation
# -------------

setup-docs: setup-virtualenv
	$(pip) install --quiet --requirement requirements-doc.txt

docs-html: setup-docs
	touch docs/index.rst
	export SPHINXBUILD="`pwd`/$(sphinx)"; cd doc; make html


# ------
# Docker
# ------

build-docker-image:
	docker build --build-arg BASE_IMAGE=avbroadcast-analyzer --tag mediatools/avbroadcast:analyzer .

publish-docker-image:
	docker tag mediatools/avbroadcast:analyzer elmyra/avbroadcast:analyzer
	docker push elmyra/avbroadcast:analyzer

run-docker-container:
	docker run --name avb --volume `pwd`:/avbroadcast --interactive --tty --rm mediatools/avbroadcast:analyzer /bin/bash

enter-docker-container:
	docker exec --interactive --tty avb /bin/bash
