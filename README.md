# Menu App project

## Running the application:
* Build docker containers (for both application and database)
```bash
docker-compose build
```
* Start the containers
```bash
docker-compose up -d
```
* Application is now available at the address [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
* API documentation is available at the address [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

* After using the application don't forget to stop the containers
```bash
docker-compose down
```
---

## Testing the application (with pytest):
* Build docker containers
```bash
docker-compose -f docker-compose-test.yml build
```
* Start the containers
```bash
docker-compose -f docker-compose-test.yml up
```
* Pytest session will start in the console
```bash
============================= test session starts ==============================
platform linux -- Python 3.10.9, pytest-7.2.1, pluggy-1.0.0
rootdir: /src
plugins: anyio-3.6.2
...
```
* After completing the test session you can stop the containers
```bash
docker-compose down
```
