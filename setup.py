from itertools import chain

from setuptools import find_packages, setup

import infmidi

EXTRAS_REQUIRE = {
    'plot': ["numpy>=1.12.0", "matplotlib>=1.5"],
    'devices': ["python-rtmidi>=1.1.0"]
}
EXTRAS_REQUIRE['all'] = list(set(chain(*EXTRAS_REQUIRE.values())))

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=infmidi.__title__,
    version=infmidi.__version__,
    author="gongyibei",
    author_email="gongyibei@gmail.com",
    license="MIT",
    description=
    "Manipulate midi and create music with a simple and high level interface.",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/gongyibei/infmidi",
    project_urls={
        "Documentation": "https://infmidi.readthedocs.io/en/latest/",
        "Code": "https://github.com/gongyibei/infmidi",
        "Issue tracker": "https://github.com/gongyibei/infmidi/issues",
    },
    packages=find_packages(),
    package_data={'': ['TimGM6mb.sf2']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
    ],
    install_requires=[
        "mido>=1.1.16",
        "sortedcontainers",
    ],
    extras_require=EXTRAS_REQUIRE,
)
