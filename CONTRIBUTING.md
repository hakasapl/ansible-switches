# Contributing

## Pre-commit

We use [pre-commit] to run a series of [linters] on the code in this
repository. These checks will be run whenever you submit a pull request. In
order to avoid delays in getting your pull request reviewed, you will want to
enable these same checks as part of your local development workflow:

1. Install the [pre-commit] tool.
1. From the root of this repository, run:

    ```
    pre-commit install
    ```

This will modify `.git/hooks/pre-commit` in your local repository to run the
pre-commit checks each time you make a commit. Among other things, these
linters will ensure consistent formatting of Python code in the repository and
alert on a variety of syntax errors.

[pre-commit]: https://pre-commit.com/
[linters]: https://en.wikipedia.org/wiki/Lint_(software)

## VLAN overlap check

CI runs `scripts/overlap.py`, which fails if any subnets in
`group_vars/all/vlans.yaml` overlap. To run it locally:

```
pip install pyyaml
python scripts/overlap.py
```

The switch drivers and their tests are in the
[ansible-stateful-switches](https://github.com/CCI-MOC/ansible-stateful-switches)
repository.
