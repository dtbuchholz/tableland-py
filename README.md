# tableland.py

[![License](https://img.shields.io/github/license/tablelandnetwork/js-template.svg)](./LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)

> A minimal Tableland Python SDK for creating, writing, and reading onchain tables

## Background

This package is a simple Tableland SDK for Python. It is designed to work with the [Tableland](https://tableland.xyz) network and uses the [web3.py](https://web3py.readthedocs.io/en/stable/) library for blockchain interacts.

## Usage

```python
from tableland import Database

# Create a new Database instance with a web3 provider and signer
signer = # TODO

db = Database(signer=signer)
```

## Development

This project uses [poetry](https://python-poetry.org/docs/#installation) for dependency management. Make sure [pipx](https://pipx.pypa.io/stable/installation/) is installed (e.g., `brew install pipx` on Mac) and then install poetry with `pipx install poetry`.

Once that's set up, you can install the project dependencies and set up the pre-commit and pre-push hooks with the following commands.

```sh
# Install dependencies
poetry install

# Setup pre-commit and pre-push hooks
poetry run pre-commit install -t pre-commit
poetry run pre-commit install -t pre-push
```

> Note: if you're using a Mac M1/M2 and the default poetry settings, you _might_ run into issues with respect to the Python virtual environment's cache directory defined in the global poetry configuration. If that's the case, running `poetry config cache-dir "$HOME/.local/share/virtualenvs"` should fix it (i.e., the previous value is `$HOME/Library/Caches/pypoetry`). Alternatively, setting the `virtualenvs.in-project` config to `true` will use a local `.venv` instead.

## Contributing

PRs accepted.

This package was created with Cookiecutter and the [sourcery.ai](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template. Small note: If editing the README, please conform to the
[standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

MIT AND Apache-2.0, © 2021-2024 Textile Contributors
