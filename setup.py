from setuptools import setup, find_packages
setup(
    name="agent-kit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["anthropic>=0.25.0"],
    entry_points={"console_scripts": ["agent-kit=agent_kit.cli:main"]},
)
