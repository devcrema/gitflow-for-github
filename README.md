# About gitflow-for-github
**ghflow** is a tool wrapped around [githubCLI](https://github.com/cli/cli) for gitflow.

In real projects, we use protection on develop and master branches to prevent mistakes and code review.
It is necessary to make a pull request when all branches are merged, but this causes a lot of iteration to make a pr when using gitflow.
**ghflow** is a tool to reduce redundant work that occurs by using **gitflow** with **PR**.

![diagram](./docs/mermaid-2021-01-03.png)

### redefine gitflow for pull-request
- Automatic tagging when release and hotfix branches are closed
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

# release finish with pull request, tag
ghflow release finish

# hotfix start
ghflow hotfix start 0.1.1

# hotfix finish with pull request, tag
ghflow hotfix finish
```

## flow summary
```
init : create master(or main), develop
feature : develop -> feature -> develop
release : develop -> release and tag -> master, develop
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
# original gitflow : tagging after merge
# it is complex with pull-request. so tagging in the release branch   
git tag 0.1.0
git push origin 0.1.0
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
git tag 0.1.1
git push origin 0.1.1
MASTER="$(git config --get master)"
DEVELOP="$(git config --get develop)"
gh pr create --base "$MASTER"
gh pr create --base "$DEVELOP"
```