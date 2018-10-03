# TASK1
awk -F: '{ print $7 " " $1}' /etc/passwd
# TASK2
### To run with docker compose run with the following commands:
``` docker-compose build ``` <br/>
``` docker-compose up --scale webapp=5 ```
### Side note:
Running in docker-compose could be slow because the implemented cache is in memory so each instance would have its own cache. We can implement a common Redis cache to solve that.