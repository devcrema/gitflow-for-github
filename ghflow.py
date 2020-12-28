#!/usr/bin/env python3

import subprocess
import sys
from enum import Enum

GIT_CONFIG_MASTER = "branch.master"
GIT_CONFIG_DEVELOP = "branch.develop"
FEATURE_PREFIX = "feature/"
RELEASE_PREFIX = "release/"
HOTFIX_PREFIX = "hotfix/"


class FlowType(Enum):
    INIT = 1
    FEATURE = 2
    RELEASE = 3
    HOTFIX = 4


def show_hint() -> None:
    print("check the readme")
    pass # TODO implements -h messages


def git_set_config(key: str, value: str) -> str:  # value
    print(f'set config: {key}:{value}')
    subprocess.run(["git", "config", "--local", key.strip(), value.strip()])
    return value


def git_get_config(key: str) -> str:  # value
    print(f'get config: {key}')
    return subprocess.run(["git", "config", "--get", key.strip()], capture_output=True, encoding="utf-8").stdout.__str__().strip()


def git_create_branch(branch_name: str) -> str:  # branch_name
    print(f'create branch: {branch_name}')
    subprocess.run(["git", "branch", branch_name.strip()])
    return branch_name


def git_checkout(branch_name: str) -> str:  # branch_name
    print(f'checkout: {branch_name}')
    subprocess.run(["git", "checkout", branch_name.strip()])
    return branch_name


def git_checkout_branch(branch_name: str) -> str:  # branch_name
    print(f'checkout -b: {branch_name}')
    subprocess.run(["git", "checkout", "-b", branch_name.strip()])
    return branch_name


def git_fetch() -> None:
    print(f'fetch')
    subprocess.run(["git", "fetch"])


def git_pull() -> None:
    print(f'pull')
    subprocess.run(["git", "pull"])


def git_push(branch_name: str) -> str:  # branch_name
    print(f'push')
    subprocess.run(["git", "push", "-u", "origin", branch_name.strip()])
    return branch_name


def git_tag(tag_name: str) -> str: # tag_name
    print(f'tag: {tag_name}')
    subprocess.run(["git", "tag", tag_name.strip()])
    return tag_name


def git_tag_push(tag_name: str) -> str: # tag_name
    print(f'push tag: {tag_name}')
    subprocess.run(["git", "push", "origin", tag_name.strip()])
    return tag_name


def git_create_pr(base_branch_name: str) -> None:
    print(f'create pr base: {base_branch_name}')
    subprocess.run(["gh", "pr", "create", "--base", base_branch_name.strip()])


def git_exist_branch(branch_name) -> bool:
    print(f'check exist branch: {branch_name}')
    return branch_name in subprocess.run(["git", "branch"], capture_output=True, encoding="utf-8").stdout.__str__()


def git_get_current_branch() -> str:
    print(f'check current branch')
    return subprocess.run(["git", "branch", "--show-current"], capture_output=True, encoding="utf-8").stdout.__str__()


def set_main_branch_with_input() -> str:
    main_branch = input("input main(master) branch name, default: main: ")
    if main_branch:
        return git_set_config(GIT_CONFIG_MASTER, main_branch)
    else:
        return git_set_config(GIT_CONFIG_MASTER, "main")


def set_develop_branch_with_input() -> str:
    develop_branch = input("input develop branch name, default: develop: ")
    if develop_branch:
        return git_set_config(GIT_CONFIG_DEVELOP, develop_branch)
    else:
        return git_set_config(GIT_CONFIG_DEVELOP, "develop")


def get_main_branch_name() -> str:
    if git_exist_branch("main"):
        return "main"
    elif git_exist_branch("master"):
        return "master"
    else:
        return set_main_branch_with_input()


def init(arguments: list[str]) -> None:
    git_fetch()
    if len(arguments) > 0 and arguments[0] == "-d":
        main_branch = get_main_branch_name()
        if not git_exist_branch(main_branch):
            git_create_branch(main_branch)
            git_push(main_branch)
        git_set_config(GIT_CONFIG_MASTER, main_branch)
        if not git_exist_branch("develop"):
            git_create_branch("develop")
            git_push("develop")
        git_set_config(GIT_CONFIG_DEVELOP, "develop")
    else:
        main_branch = set_main_branch_with_input()
        if not git_exist_branch(main_branch):
            git_create_branch(main_branch)
            git_push(main_branch)
        develop_branch = set_develop_branch_with_input()
        if not git_exist_branch(develop_branch):
            git_create_branch(develop_branch)
            git_push(develop_branch)


def feature(arguments: list[str]) -> None:
    if len(arguments) < 1:
        show_hint()
        return
    if arguments[0].upper() == "START":
        if len(arguments) < 2:
            show_hint()
            return
        feature_name = arguments[1]
        develop_branch = git_get_config(GIT_CONFIG_DEVELOP)
        git_checkout(develop_branch)
        git_pull()
        git_checkout_branch(FEATURE_PREFIX + feature_name)
    elif arguments[0].upper() == "FINISH":
        develop_branch = git_get_config(GIT_CONFIG_DEVELOP)
        git_create_pr(base_branch_name=develop_branch)
    else:
        show_hint()
        return


def release(arguments: list[str]) -> None:
    if len(arguments) < 1:
        show_hint()
        return
    if arguments[0].upper() == "START":
        if len(arguments) < 2:
            show_hint()
            return
        release_name = arguments[1]
        develop_branch = git_get_config(GIT_CONFIG_DEVELOP)
        git_checkout(develop_branch)
        git_pull()
        git_checkout_branch(RELEASE_PREFIX + release_name)
    elif arguments[0].upper() == "FINISH":
        develop_branch = git_get_config(GIT_CONFIG_DEVELOP)
        master_branch = git_get_config(GIT_CONFIG_MASTER)
        current_branch = git_get_current_branch()
        if not current_branch.startswith(RELEASE_PREFIX):
            print(f'current branch[{current_branch.strip()}] is wrong, please checkout to release branch')
            return
        release_name = current_branch.replace(RELEASE_PREFIX, "", 1)
        git_tag(release_name)
        git_tag_push(release_name)
        git_create_pr(base_branch_name=develop_branch)
        git_create_pr(base_branch_name=master_branch)
    else:
        show_hint()
        return


def hotfix(arguments: list[str]) -> None:
    if len(arguments) < 1:
        show_hint()
        return
    if arguments[0].upper() == "START":
        if len(arguments) < 2:
            show_hint()
            return
        release_name = arguments[1]
        master_branch = git_get_config(GIT_CONFIG_MASTER)
        git_checkout(master_branch)
        git_pull()
        git_checkout_branch(HOTFIX_PREFIX + release_name)
    elif arguments[0].upper() == "FINISH":
        develop_branch = git_get_config(GIT_CONFIG_DEVELOP)
        master_branch = git_get_config(GIT_CONFIG_MASTER)
        current_branch = git_get_current_branch()
        if not current_branch.startswith(HOTFIX_PREFIX):
            print(f'current branch[{current_branch.strip()}] is wrong, please checkout to hotfix branch')
            return
        hotfix_name = current_branch.removeprefix(HOTFIX_PREFIX)
        git_tag(hotfix_name)
        git_tag_push(hotfix_name)
        git_create_pr(base_branch_name=develop_branch)
        git_create_pr(base_branch_name=master_branch)
    else:
        show_hint()
        return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_hint()
        sys.exit(0)
    flow_type = FlowType[sys.argv[1].upper()]
    if flow_type == FlowType.INIT:
        init(sys.argv[2:])
    elif flow_type == FlowType.FEATURE:
        feature(sys.argv[2:])
    elif flow_type == FlowType.RELEASE:
        release(sys.argv[2:])
    elif flow_type == FlowType.HOTFIX:
        hotfix(sys.argv[2:])
    else:
        show_hint()
