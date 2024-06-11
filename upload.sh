rm -rf build
rm -rf dist
rm -rf django_miniexplorer.egg-info
pip install setuptools wheel twine
python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*
