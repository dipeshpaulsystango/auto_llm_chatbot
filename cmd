python3 -m pip install --upgrade build
python3 -m build

python3 -m pip install --upgrade twine
twine upload dist/*