# Package Usage

```{toctree}
:maxdepth: 3

job_usage.md


``` 

It is possible to use the package `indradaily` as a library in your own projects.

It's always recommended to use the package in a virtual environment. The example provided below uses a conda environment.

```sh
conda create --name indradaily python=3.10 -y
conda activate indradaily
```

You can then install the package using poetry and git. The project is not currently hosted on pypi.

```sh
poetry install git+https://github.com/dsih-artpark/indradaily.git
```

You can then import the package in your own projects.

```python
import indradaily
```









