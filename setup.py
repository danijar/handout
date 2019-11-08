import setuptools
import pathlib


setuptools.setup(
    name='handout',
    version='1.1.2',
    description='Turn Python scripts into handouts with Markdown and figures',
    url='http://github.com/danijar/handout',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    install_requires=[],
    extras_require={'media': ['imageio']},
    packages=['handout'],
    package_data={'handout': ['data/*']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'License :: OSI Approved :: Apache Software License',
    ],
)
