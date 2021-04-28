# About gitflow-for-github
**ghflow** is a tool wrapped around [githubCLI](https://github.com/cli/cli) for gitflow.

**ghflow** is a tool to reduce redundant work that occurs by using **gitflow** with **PR**.

### gitflow for pull-request
- Tagging when release and hotfix branches are closed
- When a feature or release or hotfix branch is finished, it creates a PR instead of merging it.
- Support master branch for github (main or master)

## Prerequisite
```shell
>= python 3.5
  - mac: brew install python3
  - windows: choco install python3
  
github cli (gh) [https://github.com/cli/cli]
  - mac: brew install gh
  - windows: choco install gh	
```

## how to install
```shell
pip install ghflow
```

## how to use
```shell
# init branches
ghflow init
# init with exist branches
ghflow init -d

# feature start
ghflow feature start new-feature

# feature finish with pull request
ghflow feature finish

# release start
ghflow release start 0.1.0

# release finish with pull request
ghflow release finish

# hotfix start
ghflow hotfix start 0.1.1

# hotfix finish with pull request
ghflow hotfix finish

# checkout main branch and tagging and push
ghflow tag 0.1.1
```

## flow summary
```
init : create master(or main), develop
feature : develop -> feature -> develop
release : develop -> release -> master, develop
hotfix : master -> hotfix -> master, develop
```

## init
```shell
ghflow init
```
equivalent to
```shell
git fetch
git config --local master "master"
git checkout -b master # (or main or something)
git push -u origin master # (or main or something)
git config --local develop
git checkout -b develop
git push -u origin develop
```

## feature start
```shell
ghflow feature start new-feature
```
equivalent to
```shell
DEVELOP="$(git config --get develop)"
git checkout "$DEVELOP"
git checkout -b feature/new-feature
```
## feature finish
```shell
ghflow feature finish
```
equivalent to
```shell
DEVELOP="$(git config --get develop)"
gh pr create --base "$DEVELOP"
```

## release start
```shell
ghflow release start 1.0.0
```
equivalent to
```shell
DEVELOP="$(git config --get develop)"
git checkout "$DEVELOP"
git checkout -b release/1.0.0
```
## release finish
```shell
ghflow release finish
```
equivalent to
```shell
MASTER="$(git config --get master)"
DEVELOP="$(git config --get develop)"
gh pr create --base "$MASTER"
gh pr create --base "$DEVELOP"
```
## hotfix start
```shell
ghflow hotfix start 1.0.1
```
equivalent to
```shell
MASTER="$(git config --get master)"
git checkout "$MASTER"
git checkout -b hotfix/1.0.1
```

## hotfix finish
```shell
ghflow hotfix finish
```
equivalent to
```shell
MASTER="$(git config --get master)"
DEVELOP="$(git config --get develop)"
gh pr create --base "$MASTER"
gh pr create --base "$DEVELOP"
```

## tag
```shell
ghflow tag 0.1.0
```
equivalent to
```shell
MASTER="$(git config --get master)"
git checkout "$MASTER"
git pull
git tag 0.1.0
git push origin 0.1.0
```


## deployment
```shell
# install
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine
# deploy
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```