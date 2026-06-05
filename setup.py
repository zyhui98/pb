import setuptools


with open('requirements.txt') as f:
    install_requires = [line.strip() for line in f if line.strip()]

setuptools.setup(
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=install_requires,
)
