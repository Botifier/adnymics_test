# TASK1
awk -F: '{ print $7 " " $1}' /etc/passwd
# TASK2
### To run directly:
``` pip install -r requirements.txt ```<br/>
``` cd webapp/ ```<br/>
``` python server.py ```
App will be running on localhost port 8000
### To run with docker compose run with the following commands:
``` docker-compose build ``` <br/>
``` docker-compose up --scale webapp=5 ```
HA Proxy will serve the app on port 8000
### Running Tests:
``` python webapp/server_test.py ```<br/>
``` python webapp/fibonacci_test.py ```
### Side notes:
Running in docker-compose could be slow because the implemented cache is in memory so each instance would have its own cache. We can implement a common Redis cache to solve that.<br/>
### TODO:
- Add Travis<br/>
- Add flake8 linter<br/>
- Add tox
