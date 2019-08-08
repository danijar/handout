import pathlib
import setuptools


setuptools.setup(
    name='handout',
    version='1.0.0',
    description='Turn Python scripts into handouts with Markdown and figures',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='http://github.com/danijar/handout',
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
