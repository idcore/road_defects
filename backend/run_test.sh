export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest -s $1 $2 
