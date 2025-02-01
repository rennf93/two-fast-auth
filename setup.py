import pathlib
from setuptools import (
    setup,
    find_packages
)

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="two-fast-auth",
    version="1.0.4",
    packages=find_packages(
        include=[
            "two_fast_auth",
            "two_fast_auth.*"
        ]
    ),
    install_requires=[
        "fastapi",
        "pyotp",
        "qrcode",
        "pillow",
    ],
    extras_require={
        "dev": [
            "black",
            "fastapi-users",
            "flake8",
            "httpx",
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "pytest-mock",
            "sqlalchemy"
        ]
    },
    python_requires=">=3.10",
    author="Renzo Franceschini",
    author_email="rennf93@gmail.com",
    description="FastAPI 2-Factor Authentication Middleware",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rennf93/two-fast-auth",
    # project_urls={
    #     "Documentation": "https://github.com/rennf93/two-fast-auth/blob/main/README.md",
    #     "Issue Tracker": "https://github.com/rennf93/two-fast-auth/issues",
    # },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: FastAPI",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_package_data=True,
    package_data={
        "two_fast_auth": ["py.typed"],
    },
    license="MIT",
    keywords=[
        "fastapi",
        "security",
        "2fa",
        "authentication",
        "middleware"
    ],
)
