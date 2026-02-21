"""Target-to-robot assignment logic."""
from dataclasses import dataclass
from .geometry import calculateDistance


@dataclass
class AssignmentState:
    firstTargetAttach: str = None
    secondTargetAttach: str = None
    firstTargetAttached: bool = False
    secondTargetAttached: bool = False


def computeDistances(targetCenter, robotCenters):
    """Compute distances from a target to each robot."""
    if targetCenter is None:
        return None
    distances = []
    for center in robotCenters:
        if center is None:
            distances.append(100000)
        else:
            distances.append(calculateDistance(targetCenter, center))
    return distances


def assignFirstTarget(state, distances):
    """Assign the first target to a robot."""
    if distances is None:
        state.firstTargetAttach = None
        state.firstTargetAttached = False
        return
    if distances[0] <= distances[1]:
        if not state.firstTargetAttached:
            state.firstTargetAttach = "first"
            state.firstTargetAttached = True
    elif distances[1] <= distances[0]:
        if not state.firstTargetAttached:
            state.firstTargetAttach = "second"
            state.firstTargetAttached = True
    else:
        state.firstTargetAttach = None
        state.firstTargetAttached = False


def assignSecondTarget(state, distances):
    """Assign the second target while avoiding conflicts."""
    if distances is None:
        state.secondTargetAttach = None
        state.secondTargetAttached = False
        return
    if distances[0] <= distances[1]:
        if not state.secondTargetAttached and state.firstTargetAttach != "first":
            state.secondTargetAttach = "first"
            state.secondTargetAttached = True
        if not state.secondTargetAttached and state.firstTargetAttach == "first":
            state.secondTargetAttach = "second"
            state.secondTargetAttached = True
    elif distances[1] <= distances[0]:
        if not state.secondTargetAttached and state.firstTargetAttach != "second":
            state.secondTargetAttach = "second"
            state.secondTargetAttached = True
    else:
        state.secondTargetAttach = None
        state.secondTargetAttached = False



