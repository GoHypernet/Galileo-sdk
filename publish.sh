pip install wheel
pip install twine
rm -rf build dist
python3 setup.py sdist bdist_wheel
#twine upload dist/*
