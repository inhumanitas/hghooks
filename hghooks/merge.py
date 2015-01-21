# coding: utf-8
from collections import Iterable
import json


__author__ = 'valiullin'


def matches_direction(current_branch, merging_branch, directions):
    matched = False
    for direction in directions:
        if len(direction) == 2:
            from_, to_ = direction
            if current_branch == from_ and to_ == merging_branch:
                matched = True
    return matched


def convert_param(param):
    try:
        value = json.loads(param)
    except ValueError:
        value = None

    return value


def merge_hook(repo, ui, parent1, parent2, hooktype):
    u"""Hook will forbid merges that are not suitable for repo
    Configure your hgrc with section like this example
    [branches]
        # list of brach names, must be json serializable
        # [[current, merge_with], ...]
        bad_merges = [["dev", "default"], ["test", "dev"], ["default", "test"], ["default", "dev"]]
        im_trusting_myself = false

    :parent1: A changeset ID.
        The ID of the parent that the working directory is to be updated to.
        If the working directory is being merged, it will not change this parent.
    :parent2: A changeset ID.
        Only set if the working directory is being merged.
        The ID of the revision that the working directory is being merged with.
    :hook_type: hook_type example - preupdate
    :returns: False in success, True if failure and forbid commit
    """
    failed = True
    success = False
    preupdate_type = 'preupdate'

    ctx1 = repo.changectx(parent1)
    current_branch = ctx1.branch()

    ctx2 = repo.changectx(parent2)
    merging_branch = ctx2.branch()

    merging = repo.dirstate.branch() == current_branch

    # making sure we are doing merge
    if hooktype != preupdate_type or not all([parent1, parent2]) or not merging:
        ui.debug("Merge hook will not be applied, "
                 "only for pre update while merging")
        return success

    is_iterable = lambda x: isinstance(x, Iterable)

    bad_merges = ui.config('branches', 'bad_merges')
    bad_directions = convert_param(bad_merges)

    skip_errors = ui.config('branches', 'im_trusting_myself')
    skip_errors = convert_param(skip_errors)

    if not is_iterable(bad_directions):
        ui.warn("'bad_merges' configured improperly")
        return failed

    matched = matches_direction(current_branch, merging_branch, bad_directions)

    if matched:
        ui.warn("You're going to merge the bad way, "
                "Make sure what you're doing or disable hook")
    return success if skip_errors else matched