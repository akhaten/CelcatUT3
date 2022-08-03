from distutils.core import setup


with open('requirements.txt') as f:
    requirements = f.readlines()


setup(
    name = 'CelcatUT3',
    version = 'v0.1.0',
    author = 'Jessy Khafif',
    author_email= 'khafifjessy.github@gmail.com',
    packages= [
        'Ut3'
    ],
    install_requires=requirements
)