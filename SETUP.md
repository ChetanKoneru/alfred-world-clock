## SETUP

This documentation is for those who want to set up this workflow locally to work on it. PRs are welcome!


### requirements

- macOS with the Xcode Command Line Tools (`plutil`, `/usr/bin/python3`)
- [uv](https://docs.astral.sh/uv/)

The workflow is pinned to Python 3.9 in `.python-version` because that is the
interpreter Alfred runs the workflow with (`/usr/bin/python3`).


### dependencies

Install the development environment:

```sh
uv sync
```

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`.
Add new dependencies with:

```sh
uv add <package>
```

Don't use a `requirements.txt` file.


### testing

```sh
PYTHONPATH=src uv run python -m unittest discover -s tests
```


### building the workflow

Run the release script:

```sh
./scripts/release.sh
```

This builds the workflow using the current version and opens the generated file
in Alfred when it finishes.

To build without opening Alfred:

```sh
NO_OPEN=1 ./scripts/release.sh
```

To build with a new version:

```sh
./scripts/release.sh 2.5.0
```

The release script:

1. Updates the version in `pyproject.toml`, `uv.lock`, and `info.plist`.
2. Creates or updates a dedicated `.venv-release` environment containing only runtime dependencies.
3. Runs the test suite.
4. Runs `./scripts/build.sh` to assemble the `dist/` folder.
5. Packages the workflow into `releases/`.

The release environment is separate from the development `.venv`, so building
does not remove your development tools.

Generated workflows are stored as:

```text
releases/alfred-world-clock.v<version>.alfredworkflow
```

For example:

```text
releases/alfred-world-clock.v2.5.0.alfredworkflow
```

To install a generated workflow, open it:

```sh
open releases/alfred-world-clock.v2.5.0.alfredworkflow
```

The `dist/`, `.venv/`, `.venv-release/`, and `releases/` folders are ignored by
Git.


### building only `dist/`

To rebuild the runnable files without creating a `.alfredworkflow` package:

```sh
UV_PROJECT_ENVIRONMENT=.venv-release uv sync --no-dev
VENV=.venv-release ./scripts/build.sh
```

This creates:

```text
dist/
  main.py
  data.py
  helpers.py
  formatters.py
  ...bundled dependencies
```

`info.plist` runs the workflow with `/usr/bin/python3 ./dist/main.py $@`, so the
`dist/` folder must be included at the root of the packaged workflow.
