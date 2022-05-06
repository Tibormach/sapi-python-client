from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name='kbcstorage_tibor',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    url='https://github.com/tibormach/sapi-python-client',
    download_url='https://github.com/tibormach/sapi-python-client',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'boto3',
        'azure-storage-blob',
        'requests'
    ],
    test_suite='tests',
    tests_require=['responses'],
    long_description=readme,
    license="MIT"
)
