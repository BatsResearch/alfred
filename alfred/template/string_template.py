import json
import logging
import re
from typing import Dict, Any, Optional, Iterable, List, Union

import numpy as np
import torch

from alfred.fm.query import Query, CompletionQuery, RankedQuery
from alfred.template.template import Template

logger = logging.getLogger(__name__)


class StringTemplate(Template):
    """
    Prompt Template Class for Common Static Templates

    The class handles ranked scoring and completion queries for static templates.

    .. note::
        On partial label integration:
        Partial Label vote is implicitly integrated in the template.
        Users will need to specify the label maps for the partial label group numbers.
            e.g.
            Rule: Predict "stripe" attributes for labels [zebra, tigers].
            Label Numerical: {"zebra": 1, "tiger": 2, "horse": 3}
            Prompt: "Does the [[animal]] have stripes?"

            answer_choices: "yes|||no"
            labels_map: {"yes": 2, "no": 1}

            The partial label partition would be: [[3], [1,2]]


    Methods:
        apply: apply template to an example and returns a query object
        vote: vote for the responses based on the matching function and the label maps
        update_template: update template

    Properties:
        template: template
        type: type of the template
        id: id of the template
        name: name of the template
        reference: reference
        metadata: metadata
    """

    def __init__(
            self,
            template: str,
            id: Optional[str] = None,
            name: Optional[str] = None,
            reference: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None,
            answer_choices: Optional[Union[str, List[str]]] = None,
    ):
        """

        Static Prompt Template Constructor:

        :param template: template strings with keywords enclosed in *double square brackets*
                            (e.g. "Does the [[animal]] have stripes?")
        :type template: str
        :param id: (optional) id of the template
        :type id: str
        :param name: (optional) name of the template
        :type name: str
        :param reference: (optional) reference of the template
        :type reference: str
        :param metadata: (optional) metadata of the template
        :type metadata: Dict[str, Any]
        :param answer_choices:  (optional) can be one of the following formats:
                                -  a ||| delimited string of choices that enumerates
                                   the possible completions. (PromptSource Convention)
                                   e.g. "cat ||| dog"
                                   This is for compatibility with promptsource templates
                                - a list of strings that enumerates the possible completions
                                    e.g. ["cat", "dog"]
                               If None is given, then the template is open-ended completion.
        :type answer_choices: str
        """
        self._template = template

        self._id = id
        self._name = name
        self._reference = reference
        self._metadata = metadata

        self._answer_choices = answer_choices
        self._answer_candidates = None

        self._keywords = re.findall(r"\[\[(.*?)\]\]", template)

        if answer_choices:
            if isinstance(answer_choices, str):
                self._answer_candidates = [
                    _x.strip() for _x in answer_choices.split("|||")
                ]
            elif isinstance(answer_choices, list):
                self._answer_candidates = answer_choices
            else:
                logger.warning(
                    f"Unsupported answer choices format: {type(answer_choices)}"
                )
                self._answer_choices = None

    def from_promptsource(self, promptsource_template):
        """
        Update the template from a promptsource template

        :param promptsource_template: a promptsource template
        :type promptsource_template: Dict
        """
        self._template = promptsource_template['template']
        self._id = promptsource_template['id']
        self._name = promptsource_template['name']
        self._reference = promptsource_template['reference']
        self._metadata = promptsource_template['metadata']
        self._answer_choices = promptsource_template['answer_choices']

    def apply(self, example: Dict, **kawrgs) -> Query:
        """
        Apply template to an example and returns a query object

        :param example: an example in format of dictionary
        :type example: Dict
        :param kawrgs: "key_translator" for key translation (e.g. for fields key replacements)
        :type kawrgs: Dict
        :return: query object (either CompletionQuery or RankedQuery depending on the template type)
        :rtype: Query
        """
        if 'key_translator' in kawrgs:
            key_translator = kawrgs['key_translator']
        else:
            key_translator = None

        prompt = self._template
        for key, value in example.items():
            if isinstance(value, str):
                if key_translator:
                    try:
                        k = key_translator[key]
                    except KeyError:
                        k = key
                else:
                    k = key
                prompt = prompt.replace(f"[[{str(k)}]]", value)
            elif type(value) in [list, np.ndarray, torch.Tensor]:
                if isinstance(key, int):
                    if key_translator:
                        try:
                            k = key_translator[key]
                        except KeyError:
                            k = key
                    else:
                        k = key
                    prompt[k] = value
                elif isinstance(key, str) and ':' in key:
                    start, end = key.split(':')
                    if len(start) == 0:
                        start = 0
                    if len(end) == 0:
                        end = len(prompt)
                    r = int(end) - int(start)
                    assert r == len(
                        value
                    ), f"Length of the value {len(value)} does not match the range {r}"
                    prompt[int(start):int(end)] = value
                else:
                    logger.error(
                        f"Key {key} is not an integer. Cannot replace with list."
                    )
                    raise ValueError(
                        f"Key {key} is not an integer. Cannot replace with list."
                    )

        if self._answer_choices:
            return RankedQuery(prompt=prompt,
                               candidates=self._answer_candidates)
        else:
            return CompletionQuery(prompt)

    def apply_to_dataset(
            self,
            dataset: Iterable[Dict],
            **kwargs: Any,
    ) -> Iterable[Query]:
        """
        A wrapper function to apply the template to a dataset iteratively

        :param dataset: a dataset in format of a iterable of dictionary
        :type dataset: Iterable[Dict]
        :param kwargs: Additional arguments to pass to apply
        :type kwargs: Any
        :return: an iterable of query objects
        :rtype: Iterable[Query]
        """
        return [self.apply(example, **kwargs) for example in dataset]

    def get_answer_choices_list(self) -> List[str]:
        """
        Get answer choices list

        :return: answer choices list
        :rtype: List
        """
        return self._answer_candidates

    @property
    def template(self):
        """returns the template"""
        return self._template

    @property
    def type(self):
        """returns the template type"""
        return self._type

    @property
    def keywords(self):
        """returns the keywords"""
        return self._keywords

    @property
    def id(self):
        """returns the template id"""
        return self._id

    @property
    def name(self):
        """returns the template name"""
        return self._name

    @property
    def reference(self):
        """returns the template reference"""
        return self._reference

    @property
    def metadata(self):
        """returns the template metadata"""
        return self._metadata

    def serialize(self):
        """
        returns the template as a json string of dictionary

        :return: json string of dictionary
        :rtype: str
        """
        return json.dumps({
            "id": self._id,
            "name": self._name,
            "reference": self._reference,
            "template": self._template,
            "metadata": self._metadata,
            "answer_choices": self._answer_choices,
        })

    def deserialize(self, json_str: str) -> Template:
        """
        returns a template object from a json string of dictionary

        :param json_str: json string of dictionary to deserialize a string template
        :type json_str: str
        :return: template object
        """
        json_str = json.loads(json_str)
        self.__init__(
            json_str['id'],
            json_str['name'],
            json_str['reference'],
            json_str['template'],
            json_str['metadata'],
            json_str['answer_choices'],
        )
        return self

    def __call__(
            self,
            example: Dict,
            **kawrgs: Any,
    ) -> Query:
        """
        A wrapper function to apply the template to a single example

        :param example: a single example in format of a dictionary
        :type example: Dict
        :param kawrgs: Additional arguments to pass to apply
        :type kawrgs: Any
        :return: a query object
        :rtype: Query
        """
        return self.apply(example, **kawrgs)
