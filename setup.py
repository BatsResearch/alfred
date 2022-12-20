from setuptools import setup, find_packages

setup(
    name='Alfred',
    version='0.0.1',
    # url='https://github.com/dotpyu/alfred',
    author='Peilin Yu',
    author_email='peilin_yu@brown.edu',
    description='Foundation Model Prompting for Weak Supervisions',
    packages=find_packages(),
    install_requires=['numpy >= 1.11', 'scipy >= 1.5', 'torch >= 1.4', 'tqdm >= 4.62.3', 'torchvision >= 0.10'],
)
