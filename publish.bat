rem pip install --upgrade build
rem pip install --upgrade twine

rmdir /S /Q dist
rmdir /S /Q build
rmdir /S /Q qgate_graph.egg-info

rem helper 'https://www.scivision.dev/python-minimal-package/'
rem https://pypa-build.readthedocs.io/en/latest/
python -m build --wheel

rem twine upload is supported
twine upload dist/* --verbose -u__token__
