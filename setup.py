from __future__ import annotations

import setuptools

with open('requirements.txt', encoding='UTF-8') as f:
    install_requires = f.read().strip().splitlines()
with open('README.md', encoding='UTF-8') as f:
    long_description = f.read().strip()
with open('CHANGELOG.md', encoding='UTF-8') as f:
    long_description += f'\n\n---\n\n{f.read().strip()}\n'

setuptools.setup(
    name='HDRezka',
    version='2.0.1',

    author='Nikita (NIKDISSV)',
    author_email='nikdissv@proton.me',

    description='HDRezka (rezka.ag) Python API',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/NIKDISSV-Forever/HDRezka',
    project_urls={
        'GitHub': 'https://github.com/NIKDISSV-Forever/HDRezka',
        'Documentation': 'https://nikdissv-forever.github.io/HDRezka/hdrezka'
    },
    packages=setuptools.find_packages(),
    install_requires=install_requires,

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Video',

    ],

    python_requires='>=3.10',
    keywords=['HDRezka', 'rezka.ag', 'watch online', 'api', 'stream']
)
