from setuptools import setup, find_packages


def get_reqs(req_file):
    with open(req_file) as f:
        return [line for line in f]


setup(
    name='numerology',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=get_reqs('requirements.txt')
)
