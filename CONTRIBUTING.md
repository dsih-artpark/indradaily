# Contributing

Contributions are welcome and are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute to the project in the following ways:

- Report bugs and errors
- Suggest improvements and new features
- Write documentation
- Write code
- Write tests

## Writing code

To write code, you can use the following steps:

1. Fork the repository into your own GitHub account/organization.
2. Clone the repository to your local machine and checkout a new branch for the contribution you're working on.
3. Make your changes and commit them.
4. Push your changes to the relevant branch in your fork.
5. Create a pull request on GitHub to the development branch of the main repository. Pull requests to the production branch will not be accepted.


It is recommended to use a virtual environment to write code. The project uses conda for this purpose, but you can use any other virtual environment manager. 
You are however required to use poetry to install the dependencies and to run the tests. You can install poetry using pipx, or checkout the [official installation guide](https://python-poetry.org/docs/#installation).

```sh
pipx install poetry
```

You can then create a conda environment (or any other virtual environment) and install the dependencies. For conda, you can use [miniconda3](https://docs.conda.io/en/latest/miniconda.html) for a lightweight installation.

```sh
conda create --name indradaily_dev python=3.10 -y
conda activate indradaily_dev
```

```sh
poetry install
```

## Writing Documentation

Documentation is always welcome! You can contribute to the documentation by writing documentation for the code you write or by improving the existing documentation.

Documentation is written in the `docs/source` folder and is written in [`MyST Markdown`](https://myst-parser.readthedocs.io/en/latest/), which is a dialect of Markdown that is compatible with Sphinx. 

If you're writing docs, make sure to install the docs dependencies.

```sh
conda create --name indradaily_docs python=3.10 -y
conda activate indradaily_docs
```

```sh
poetry install --with docs
```

You can then build the documentation locally using sphinx.

```sh
poetry run sphinx-build -b html docs/source docs/build
```

You can then view the documentation locally by opening the `docs/build/index.html` file in your browser.
