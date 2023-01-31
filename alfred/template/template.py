import abc


class Template(abc.ABC):
    """
    Generic interface for prompt template

    The class mirrors main functionality of promptsource's template
    Please see https://github.com/bigscience-workshop/promptsource for more details

    @misc{bach2022promptsource,
      title={PromptSource: An Integrated Development Environment and Repository for Natural Language Prompts},
      author={Stephen H. Bach and Victor Sanh and Zheng-Xin Yong and Albert Webson and Colin Raffel and Nihal V. Nayak and Abheesht Sharma and Taewoon Kim and M Saiful Bari and Thibault Fevry and Zaid Alyafeai and Manan Dey and Andrea Santilli and Zhiqing Sun and Srulik Ben-David and Canwen Xu and Gunjan Chhablani and Han Wang and Jason Alan Fries and Maged S. Al-shaibani and Shanya Sharma and Urmish Thakker and Khalid Almubarak and Xiangru Tang and Xiangru Tang and Mike Tian-Jian Jiang and Alexander M. Rush},
      year={2022},
      eprint={2202.01279},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
    }
    """
    @property
    @abc.abstractmethod
    def template(self):
        """returns the template string"""
        pass

    @property
    @abc.abstractmethod
    def type(self):
        """returns the type of the template"""
        pass

    @property
    @abc.abstractmethod
    def keywords(self):
        """returns the keywords of the template"""
        pass

    @property
    @abc.abstractmethod
    def id(self):
        """returns the id of the template"""
        pass

    @property
    @abc.abstractmethod
    def name(self):
        """returns the name of the template"""
        pass

    @property
    @abc.abstractmethod
    def reference(self):
        """returns the reference of the template"""
        pass

    @property
    @abc.abstractmethod
    def metadata(self):
        """returns the metadata of the template"""
        pass

    @abc.abstractmethod
    def get_answer_choices_list(self, example):
        """returns the answer choices list of the template"""
        pass

    @abc.abstractmethod
    def apply(self, example):
        """returns the template applied to the example"""
        pass

    @abc.abstractmethod
    def serialize(self):
        """returns the serialized version of the template"""
        pass

    @abc.abstractmethod
    def deserialize(self, json_str):
        """returns the deserialized version of the template"""
        pass

    def __call__(self, example):
        """returns the template applied to the example, this allows a functional style"""
        return self.apply(example)
