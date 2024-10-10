from setuptools import setup, find_packages

setup(
    name='Alfred',
    version='1.0.1',
    url='https://github.com/BatsResearch/alfred',
    author='Peilin Yu',
    author_email='peilin_yu@brown.edu',
    description='Toolkit for Prompted Weak Supervisions',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'torch', 'tqdm', 'torchvision', "accelerate", "paramiko>=2.7.2", "pyarrow>=3.0.0", "grpcio", "protobuf=5.27.0"],
)
