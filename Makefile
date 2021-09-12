ENV_DIR=.venv
PYTHON=$(shell which python)
PYTHON_VERSION=$(shell python --version)

.PHONY: python-info
## Print which python is used
python-info:
	@echo "Using python from ${PYTHON}"
	@echo "Python version is ${PYTHON_VERSION}"
	activate-env

### ENVIRONMENT MANAGEMENT ###

.PHONY: create-env
## Create virtual environment
create-env:
	@virtualenv -p ${PYTHON} .venv
	. ${ENV_DIR}/bin/activate && pip install -r requirements.txt
	@echo "execute \"source ${ENV_DIR}/bin/activate\" to activate environment"

.PHONY: activate-env
## Activate virtual environment
activate-env:
	@echo "execute \"source ${ENV_DIR}/bin/activate\" to activate environment"

.PHONY: clean-env
## Remove virtual environment
clean-env:
	@rm -rf ${ENV_DIR}

.PHONY: refresh-env
## Refresh virtual environment
refresh-env: clean-env create-env

.PHONY: update-env
## Update virtual environment
update-env:
	. ${ENV_DIR}/bin/activate && pip install -r requirements.txt

### PACKAGE MANAGEMENT ###

.PHONY: dist-wheel
## Build wheel artifact
dist-wheel:
	@${PYTHON} setup.py check
	@${PYTHON} setup.py bdist_wheel

.PHONY: clean-dist
## Clean distribution folders
clean-dist:
	-@${PYTHON} setup.py clean --all
	-@rm -rf {build,dist,*.egg-info}

.PHONY: install-e
## Install package as editable
install-e:
	@${PYTHON} -m pip install -e .

.PHONY: help
# Adapted by David Prihoda from: https://raw.githubusercontent.com/nestauk/patent_analysis/3beebda/Makefile
## Auto-generated help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| less $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')