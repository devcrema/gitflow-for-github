# gitflow-for-github
- wrap github CLI for gitflow
- redefine gitflow for pull-request

## how to install (in-progress)
```shell

```

## how to use
```shell
ghflow init
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
ghflow hotfix finish 0.1.1
```

## flow summary
```
init : create master(or main), develop
feature : develop -> feature -> develop
release : develop -> release and tag -> master, develop
hotfix : master -> hotfix -> master, develop
```

## init (in-progress)
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

## feature start (in-progress)
```shell
ghflow feature start new-feature
```
equivalent to
```shell
DEVELOP="$(git config --get develop)"
git checkout "$DEVELOP"
git checkout -b feature/new-feature
```
## feature finish (in-progress)
```shell
ghflow feature finish
```
equivalent to
```shell
DEVELOP="$(git config --get develop)"
gh pr create --base "$DEVELOP"
```

## release start (in-progress)
```shell
ghflow release start 1.0.0
```
equivalent to
```shell
DEVELOP="$(git config --get develop)"
git checkout "$DEVELOP"
git checkout -b release/1.0.0
```
## release finish (in-progress)
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
## hotfix start (in-progress)
```shell
ghflow hotfix start 1.0.1
```
equivalent to
```shell
MASTER="$(git config --get master)"
git checkout "$MASTER"
git checkout -b hotfix/1.0.1
```

## hotfix finish (in-progress)
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