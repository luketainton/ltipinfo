from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='ltipinfo',
    version='1.6.0',
    description='Get information about a specified IP address or domain name',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GPLv3',
    packages=find_packages(),
    author='Luke Tainton',
    author_email='luke@tainton.uk',
    keywords=['bgp', 'ip', 'ipv4', 'lookup', 'networking'],
    url='https://github.com/luketainton/ltipinfo',
    download_url='https://pypi.org/project/ltipinfo/'
)

install_requires = []
with open('requirements.txt') as req_file:
    for line in req_file:
        install_requires.append(line)

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
