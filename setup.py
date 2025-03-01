from setuptools import setup, find_packages

def long_description() -> str:
    long_description: str = ''
    with open('README.md', 'r', encoding='utf-8') as file:
        long_description += file.read()
    with open('CHANGELOG.md', 'r', encoding='utf-8') as file:
        long_description += f'\n\n{file.read()}'
    return long_description

setup(
    name='awesomeNations',
    version='2.0.0',
    description='A simple and cozy wrapper for NationStates',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='Orly Neto',
    author_email='orly2carvalhoneto@gmail.com',
    license='MIT License',
    keywords=['NationStates', 'API wrapper', 'NationStates wrapper'],
    packages=find_packages(),
    install_requires=["urllib3==2.3.0", "xmltodict==0.14.2"])