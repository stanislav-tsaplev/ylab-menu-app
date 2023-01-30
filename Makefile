DOCKER_COMPOSE_APP := docker-compose-app.yml
DOCKER_COMPOSE_TEST := docker-compose-test.yml


.PHONY: build-app
build-app:
	docker-compose -f $(DOCKER_COMPOSE_APP) build

.PHONY: build-test
build-test:
	docker-compose -f $(DOCKER_COMPOSE_TEST) build

.PHONY: build-both
build-both:
	docker-compose -f $(DOCKER_COMPOSE_APP) build
	docker-compose -f $(DOCKER_COMPOSE_TEST) build


.PHONY: up-app
up-app:
	docker-compose -f $(DOCKER_COMPOSE_APP) up -d

.PHONY: up-test
up-test:
	docker-compose -f $(DOCKER_COMPOSE_TEST) up -d

.PHONY: up-both
up-both:
	docker-compose -f $(DOCKER_COMPOSE_APP) up -d
	docker-compose -f $(DOCKER_COMPOSE_TEST) up -d


.PHONY: down-app
down-app:
	docker-compose -f $(DOCKER_COMPOSE_APP) down

.PHONY: down-test
down-test:
	docker-compose -f $(DOCKER_COMPOSE_TEST) down

.PHONY: down-both
down-both:
	docker-compose -f $(DOCKER_COMPOSE_APP) down
	docker-compose -f $(DOCKER_COMPOSE_TEST) down


.PHONY: show-app-logs
show-app-logs:
	docker-compose -f $(DOCKER_COMPOSE_APP) logs -f api

.PHONY: show-test-logs
show-test-logs:
	docker-compose -f $(DOCKER_COMPOSE_TEST) logs -f api-test
