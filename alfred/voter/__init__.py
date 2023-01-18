from typing import List

import alfred.registry as registry
from .voter import Voter


def get_voters() -> List[Voter]:
    return registry.voters()
