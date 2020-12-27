#!/bin/sh

CURRENT_BRANCH="$(git branch --show-current)"
FLOW="$1" # init, feature, release ...
METHOD="$2" # start, finish
PARAMETER="$3" # feature name,

get_main_branch(){
  MAIN_BRANCH="$(git branch | grep -w main)"
  MASTER_BRANCH="$(git branch | grep -w master)"
  if [ "$MAIN_BRANCH" ]; then
    echo "main"
  elif [ "$MASTER_BRANCH" ]; then
    echo "master"
  fi
}

make_release(){
  case $CURRENT_BRANCH in
    "release/"*)
      git tag "${CURRENT_BRANCH#"release/"}"
      git push origin tag "${CURRENT_BRANCH#"release/"}"
      echo "create pr for develop"
      gh pr create --base develop
      echo "create pr for master"
      gh pr create --base master
     ;;
    *)
      echo "this is not release branch: $CURRENT_BRANCH"
    ;;
  esac
}

echo "current branch is $CURRENT_BRANCH"
echo "$( get_main_branch )"

# TODO init
# TODO feature start name [<base>]
# TODO feature finish name
# TODO release start name [<base>]
# TODO release finish name
# TODO hotfix start name [<base>]
# TODO hotfix finish name
#echo $1
#echo $2
#echo $3
#echo $4

