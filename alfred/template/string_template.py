import json
import logging
from typing import Dict, Any, Optional, Iterable, Callable, Union, List

import numpy as np
import torch
from tqdm.auto import tqdm

from alfred.fm.query import Query, CompletionQuery, RankedQuery
from alfred.fm.response import Response, RankedResponse, CompletionResponse
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
            Prompt: "Does the [animal] have stripes?"

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

    def __init__(self,
                 template: str,
                 id: Optional[str] = None,
                 name: Optional[str] = None,
                 reference: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None,
                 answer_choices: Optional[str] = None,
                 label_maps: Optional[Dict] = None,
                 matching_fn: Optional[Callable] = lambda x, y: x == y,
                 ):
        """

        Static Prompt Template Constructor:

        :param template: template TODO: Use jinja as soon as possible!!
        :type template: str
        :param id: (optional) id of the template
        :type id: str
        :param name: (optional) name of the template
        :type name: str
        :param reference: (optional) reference of the template
        :type reference: str
        :param metadata: (optional) metadata of the template
        :type metadata: Dict[str, Any]
        :param answer_choices:  (optional) a ||| delimited string of choices that enumerates
                                   the possible completions. (PromptSource Convention)
                                   e.g. "cat ||| dog"
                               If None is given, then the template is open-ended completion.
        :type answer_choices: str
        :param label_maps: (optional) There are 2 scenario each corresponding to ranked scoring scheme and completion scheme.
                            1. Ranked Scoring Scheme:
                                A dictionary of *labels* that maps to numerical vote/labels.
                                To use when the given answer_choices is out of order.
                                e.g. {"dog": 1, "cat": 2}
                            2. Completion Scheme:
                                A dictionary that maps *completions* to numerical values for votes.
                                e.g. {"cat": 1, "kitten": 1, "dog": 2, "puppy": 2}
        :type label_maps: Dict
        """
        self._template = template

        self._id = id
        self._name = name
        self._reference = reference
        self._metadata = metadata

        self._answer_choices = answer_choices
        self._answer_candidates = None

        if answer_choices:
            if isinstance(answer_choices, str):
                self._answer_candidates = [
                    _x.strip() for _x in answer_choices.split("|||")]
            else:
                logger.warning(
                    f"Unsupported answer choices format: {type(answer_choices)}")
                self._answer_choices = None

        self._label_maps = label_maps
        self._matching_fn = matching_fn

    def apply(self,
              example: Dict,
              **kawrgs) -> Query:
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
                prompt = prompt.replace(f"[{str(k)}]", value)
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
                        value), f"Length of the value {len(value)} does not match the range {r}"
                    prompt[int(start):int(end)] = value
                else:
                    logger.error(
                        f"Key {key} is not an integer. Cannot replace with list.")
                    raise ValueError(
                        f"Key {key} is not an integer. Cannot replace with list.")

        if self._answer_choices:
            return RankedQuery(
                prompt=prompt,
                candidates=self._answer_candidates)
        else:
            return CompletionQuery(prompt)

    def apply_to_dataset(self,
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

    def vote(self,
             responses: Union[Iterable[str],
                              str,
                              Iterable[Response],
                              Response],
             matching_function: Callable = lambda x, y: x == y,
             label_maps: Optional[Dict] = None,
             **kwargs: Any) -> np.ndarray:
        """
        Vote for the responses based on the matching function and the label maps

        *NOTE*: if label maps contains numerical labels then the vote will be the exact specified value
        if not the vote will be the index + 1 of the matched answer choice

        *Abstention vote is 0*

        *NOTE* on partial labels:

        :param responses: list of response objects
        :type responses: Union[Iterable[str], str, Iterable[Response], Response]
        :param matching_function: (optional) function to match responses against answer choices, defaulting to exact match
                                    e.g. lambda x, y: x == y
        :type matching_function: Callable
        :param label_maps: (optional) label maps that maps responses content to labels
                           label_maps specified here will overide the label_maps initialized in the template
        :type label_maps: Dict
        :return: numpy ndarray of votes in np.int8
        :rtype: np.ndarray
        """
        label_maps = self._label_maps if label_maps is None else label_maps

        if isinstance(responses, str) or isinstance(responses, Response):
            responses = [responses]

        if label_maps is None:
            logger.warning(
                "No answer label map found, voting will not be done")
            raise ValueError(
                "No answer label map found, voting will not be done")

        no_tqdm = kwargs.get('no_tqdm', True)

        if 'zero_abstention' in kwargs:
            zero_abstention = kwargs['zero_abstention']

        votes = np.zeros(len(responses))
        for idx, response in enumerate(tqdm(responses, disable=no_tqdm)):
            if type(response) in [CompletionResponse, RankedResponse]:
                response = response.prediction
            elif isinstance(response, str):
                pass
            else:
                logger.error(f"Unsupported response type: {type(response)}")
                raise ValueError(
                    f"Unsupported response type: {type(response)}")

            if isinstance(label_maps, dict):
                for k_idx, key in enumerate(label_maps.keys()):
                    if matching_function(response, key):
                        votes[idx] = label_maps[key] if isinstance(
                            label_maps[key], int) else k_idx + 1
            else:
                if matching_function(response, label_maps):
                    votes[idx] = 1
        return votes

    def get_answer_choices_list(self) -> List[str]:
        """
        Get answer choices list

        :return: answer choices list
        :rtype: List
        """
        return self._answer_candidates

    def template(self):
        """returns the template"""
        return self._template

    def type(self):
        """returns the template type"""
        return self._type

    def id(self):
        """returns the template id"""
        return self._id

    def name(self):
        """returns the template name"""
        return self._name

    def reference(self):
        """returns the template reference"""
        return self._reference

    def metadata(self):
        """returns the template metadata"""
        return self._metadata

    def serialize(self):
        """
        returns the template as a json string of dictionary

        :return: json string of dictionary
        :rtype: str
        """
        return json.dumps(
                            {
                                "id": self._id,
                                "name": self._name,
                                "reference": self._reference,
                                "template": self._template,
                                "metadata": self._metadata,
                                "answer_choices": self._answer_choices,
                                "label_maps": self._label_maps
                            }
                        )

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
            json_str['label_maps'])
        return self

    def __call__(self,
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
