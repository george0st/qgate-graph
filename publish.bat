pip install --upgrade setuptools wheel
pip install --upgrade twine

rm dist/*

python setup.py sdist bdist_wheel
twine upload dist/* --verbose -ugeorge0st
