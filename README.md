# Menu App project

## Running the application:
* Build docker containers (for both application and database)
```bash
make build-app
```
* Start the containers
```bash
make up-app
```
* Application is now available at the address [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
* API documentation is available at the address [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

* After using the application don't forget to stop the containers
```bash
make down-app
```
---

## Testing the application (with pytest):
* Build docker containers
```bash
make build-test
```
* Start the containers
```bash
make up-test
```
* Pytest session will start in the background  

* Now you can see the test results
```bash
make show-test-logs
```
* After completing the test session you can stop the containers
```bash
make down-test
```
---

## Doing both things together:
* Build docker containers
```bash
make build-both
```
* Start the containers
```bash
make up-both
```
* Application is now available at the address [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
* API documentation is available at the address [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
* At the same time Pytest session has started in the background  

* You can see the test results
```bash
make show-test-logs
```
* Once you have done all you need to do, you can stop the containers
```bash
make down-both
```
