from setuptools import setup

__version__ = "0.1"

setup(
    name="kobert-tokenizer",
    version=__version__,
    url="https://github.com/SKTBrain/KoBERT",
    license="Apache-2.0",
    author="SeungHwan Jung",
    author_email="digit82@gmail.com",
    description="Korean BERT pre-trained cased (KoBERT) for HuggingFace",
    packages=[
        "kobert_tokenizer",
    ],
    long_description="KoBERT tokenizer package for HuggingFace-compatible usage.",
    zip_safe=False,
    include_package_data=True,
)
