from setuptools import setup

with open('README.md', 'r') as fh:
    readme = fh.read()

with open('submv/_version.py') as f:
    exec(f.read())
    
args = dict(name='submv',
            version=__version__,
            description='Subtitle shift for resynchronization',
            long_description=readme,
            long_description_content_type='text/markdown',
            author='Joris Paret',
            author_email='joris.paret@gmail.com',
            maintainer='Joris Paret',
            url='https://github.com/jorisparet/submv',
            keywords=['subtitle', 'sub', 'srt', 'shift',
                      'move', 'synchronization', 'sync'],
            entry_points={'console_scripts':
                          ['submv = submv.main:main']},
            license='GPLv3',
            classifiers=[
                'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                'Development Status :: 3 - Alpha',
                'Topic :: Utilities ',
                'Programming Language :: Python :: 3',
                'Operating System :: POSIX :: Linux',
                'Operating System :: Microsoft :: Windows',
                'Intended Audience :: End Users/Desktop',
                'Natural Language :: English']
)

setup(**args)
