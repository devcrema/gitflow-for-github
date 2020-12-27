#!/usr/bin/env python3

import subprocess
import sys
from enum import Enum


class FlowType(Enum):
    INIT = 1
    FEATURE = 2
    RELEASE = 3
    HOTFIX = 4


def set_config(key: str, value: str) -> str:  # value
    subprocess.run(["git", "config", "--local", key, value])
    return value


def get_config(key: str) -> str:  # value
    return subprocess.run(["git", "config", "--get", key], capture_output=True).stdout.__str__()


def create_branch(branch_name: str) -> str:  # branch_name
    subprocess.run(["git", "branch", branch_name])
    return branch_name


def checkout(branch_name: str) -> str:  # branch_name
    subprocess.run(["git", "checkout", branch_name])
    return branch_name


def fetch() -> None:
    subprocess.run(["git", "fetch"])


def push(branch_name: str) -> str:  # branch_name
    subprocess.run(["git", "push", "-u", "origin", branch_name])
    return branch_name


def create_pr(base_branch_name: str) -> None:
    subprocess.run(["gh", "pr", "create", "--base", base_branch_name])


def exist_branch(branch_name) -> bool:
    return branch_name in subprocess.run(["git", "branch"], capture_output=True).stdout.__str__()


def set_main_branch_with_input() -> str:
    main_branch = input("input main(master) branch name, default: main: ")
    if main_branch:
        return set_config("branch.master", main_branch)
    else:
        return set_config("branch.master", "main")


def set_develop_branch_with_input() -> str:
    develop_branch = input("input develop branch name, default: develop: ")
    if develop_branch:
        return set_config("branch.develop", develop_branch)
    else:
        return set_config("branch.develop", "develop")


def get_main_branch_name() -> str:
    if exist_branch("main"):
        return "main"
    elif exist_branch("master"):
        return "master"
    else:
        return set_main_branch_with_input()


def init(arguments: list[str]) -> None:
    fetch()
    if len(arguments) > 0 and arguments[0] == "-d":
        main_branch = get_main_branch_name()
        if not exist_branch(main_branch):
            create_branch(main_branch)
            set_config("branch.main", main_branch)
            push(main_branch)
        if not exist_branch("develop"):
            create_branch("develop")
            set_config("branch.develop", "develop")
            push("develop")
    else:
        main_branch = set_main_branch_with_input()
        if not exist_branch(main_branch):
            create_branch(main_branch)
            push(main_branch)
        develop_branch = set_develop_branch_with_input()
        if not exist_branch(develop_branch):
            create_branch(develop_branch)
            push(develop_branch)


def feature(arguments: list[str]) -> None:
    pass # TODO


def release(arguments: list[str]) -> None:
    pass # TODO


def hotfix(arguments: list[str]) -> None:
    pass # TODO


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("how to use")  # TODO implements -h messages
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
        print("how to use")  # TODO implements -h messages
