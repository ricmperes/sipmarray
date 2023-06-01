from setuptools import setup, find_packages

def open_requirements(path):
    with open(path) as f:
        requires = [
            r.split('/')[-1] if r.startswith('git+') else r
            for r in f.read().splitlines()]
    return requires

requires = open_requirements('requirements.txt')
setup(
    name='sipmarray',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='BSD-3-Clause license',
    description='A simple package to get the geometry of SiPM arrays.',
    long_description=open('README.md').read(),
    install_requires=requires,
    url='https://github.com/ricmperes/sipmarray',
    author='Ricardo Peres',
    author_email='rperes@physik.uzh.ch'
)