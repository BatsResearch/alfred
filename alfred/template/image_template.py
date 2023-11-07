import json
import logging
from typing import Dict, Any, Optional, Iterable, List, Union, Tuple

import numpy as np
import torch
from PIL import Image

from alfred.fm.query import Query, RankedQuery
from alfred.template.template import Template

logger = logging.getLogger(__name__)


class ImageTemplate(Template):
    """
    Template Class for Image data

    The class handles ranked queries for image data.
    """

    def __init__(
        self,
        candidate_replacement: dict,
        template: str = "A photo of [[label]]",
        id: Optional[str] = None,
        name: Optional[str] = None,
        reference: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """

        Static Image Prompt Template Constructor:

        Usage:
            >>> candidate_replacement = {"label": ["cat", "dog"]}
            >>> template = "A photo of [[label]]"
            >>> image_template = ImageTemplate(candidate_replacement, template)


        :param candidate_replacement: a dictionary of candidate replacement
        :type candidate_replacement: dict
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
        """

        self._template = template

        self._id = id
        self._name = name
        self._reference = reference
        self._metadata = metadata

        self._candidate_replacement = candidate_replacement
        self._template = template

        self._templated_candidates = []
        for keyword, candidates in self._candidate_replacement.items():
            for candidate in candidates:
                self._templated_candidates.append(
                    self._template.replace(f"[[{keyword}]]", f"{candidate}")
                )

    def apply(
        self,
        example: Union[Image.Image, torch.tensor, np.ndarray, str, tuple],
        keyword: str = "image_path",
        **kwargs: Any,
    ) -> RankedQuery:
        """
        Apply the template to a single image example

        :param example: a single example in format of a dictionary
        :type example: PIL Image, torch.tensor, numpy.ndarray, str, tuple
        :param kwargs: Additional arguments to pass to apply
        :type kwargs: Any
        :return: a RankedQuery object
        :rtype: RankedQuery
        """
        if isinstance(example, Image.Image):
            image = example
        elif isinstance(example, torch.Tensor):
            image = Image.fromarray(example.numpy())
        elif isinstance(example, np.ndarray):
            image = Image.fromarray(example)
        elif isinstance(example, Tuple):
            image = example[0]
        elif isinstance(example, Dict):
            image = Image.open(example[keyword])
        elif isinstance(example, str):
            image = Image.open(example)
        else:
            raise ValueError(f"Unsupported example type: {type(example)}")

        return RankedQuery(image, self._templated_candidates)

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
        return json.dumps(
            {
                "id": self._id,
                "name": self._name,
                "reference": self._reference,
                "template": self._template,
                "metadata": self._metadata,
                "candidate_replacement": self._candidate_replacement,
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
            json_str["id"],
            json_str["name"],
            json_str["reference"],
            json_str["template"],
            json_str["metadata"],
            json_str["candidate_replacement"],
        )
        return self

    def __call__(
        self,
        example: Union[Image.Image, torch.tensor, np.ndarray, str, tuple],
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
