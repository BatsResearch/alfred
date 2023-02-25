from setuptools import setup, find_packages

setup(
    name='Alfred',
    version='0.0.1',
    url='https://github.com/BatsResearch/alfred',
    author='Peilin Yu',
    author_email='peilin_yu@brown.edu',
    description='Toolkit for Prompted Weak Supervisions',
    packages=find_packages(),
    install_requires=['numpy >= 1.11', 'scipy >= 1.5', 'torch >= 1.4', 'tqdm >= 4.62.3', 'torchvision >= 0.10'],
)
