from setuptools import setup, find_packages

setup(
    name="landscape_lab",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'fastapi',
        'uvicorn[standard]',
        'sqlalchemy',
        'python-multipart',
        'python-jose[cryptography]',
        'passlib[bcrypt]',
        'pillow',
        'ezdxf',
        'trimesh'
    ],
    entry_points={
        'console_scripts': [
            'landscape-lab=landscape_lab.cli:main',
        ],
    },
    package_data={
        'landscape_lab': [
            'database/*.py',
            'models/*.py',
            'templates/*.html',
            'static/css/*',
            'static/js/*'
        ]
    }
)
