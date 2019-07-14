# DOCKER
docker build -t recommendation .
docker run -p 8000:80 recommendation

# ORIGINAL (LINUX)
pip install --trusted-host pypi.python.org -r requirements.txt
python3 /worker/task.py & python3 manage.py runserver
