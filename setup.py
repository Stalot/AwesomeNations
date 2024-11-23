from setuptools import setup, find_packages

def description():
    desc: str
    with open('README.md', 'r') as file:
        desc += file.read()
    return desc



setup(
    name='awesomeNations',
    version='0.0.4',
    description='A simple python web scraping library for NationStates',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='LyTech',
    author_email='orly2carvalhoneto@gmail.com',
    keywords='NationStates',
    packages=find_packages(),
    install_requires=['beautifulsoup4==4.12.3', 'requests==2.32.3'])