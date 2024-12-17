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
    author='Orly Neto',
    author_email='orly2carvalhoneto@gmail.com',
    license='MIT License',
    keywords=['NationStates', 'Scrapper', 'Web Scrapper'],
    packages=find_packages(),
    install_requires=['beautifulsoup4==4.12.3', 'requests==2.32.3', 'selenium==4.27.1', 'webdriver-manager==4.0.2'])