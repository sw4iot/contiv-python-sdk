import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()


def load_reqs(filename):
    with open(filename) as reqs_file:
        return [
            re.sub('==', '>=', line) for line in reqs_file.readlines()
            if not re.match('\s*#', line)
        ]


requirements = load_reqs('requirements.txt')

setuptools.setup(
    name="contiv-sdk",
    version="0.0.3",
    author="SOFTWAY4IoT",
    author_email="softway4iot@gmail.com",
    description="contiv-python-sdk of SOFTWAY4IoT",
    license="Apache Software License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sw4iot/contiv-python-sdk",
    install_requires=requirements,
    packages=[
        'contiv_sdk'
    ],
    package_dir={
        'contiv_sdk': 'contiv_sdk'
    },
    keywords='contiv-sdk',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)
