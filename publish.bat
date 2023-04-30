#pip install --upgrade setuptools wheel
#pip install --upgrade twine

rmdir /S /Q dist

# new sytax => python -m build (with build)
python setup.py sdist bdist_wheel
# twine upload dist/* --verbose -ugeorge0st
