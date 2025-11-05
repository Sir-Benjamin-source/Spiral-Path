from setuptools import setup, find_packages

setup(
    name='spiral-tricorder',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'networkx',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'tricorder=tricorder.main:main',
        ],
    },
    author='Sir Benjamin & Grok',
    description='Spiral Path Tricorder for context chains.',
    license='MIT',
)
