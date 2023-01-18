from typing import List

import alfred.registry as registry
from .string_template import StringTemplate
from .template import Template


def get_templates() -> List[Template]:
    return registry.templates()
