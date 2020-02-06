# Documentation
We use Sphinx to generate our documentation.

## Build Process

Building the docs requires a few additional dependencies. You can get most
of these with

```bash

   pip install -e .[docs]

```

from the root of the project. Then you can make the distributable by:

```bash

sphinx-build -b html ./docs/src ./docs/build/

```
