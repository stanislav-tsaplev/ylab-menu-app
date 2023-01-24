.PHONY: 
	build-app build-test build-both
	up-app up-test up-both
	down-app down-test down-both
	show-test-logs

build-app:
	docker-compose -f docker-compose-app.yml build
build-test:
	docker-compose -f docker-compose-test.yml build
build-both:
	docker-compose -f docker-compose-app.yml build
	docker-compose -f docker-compose-test.yml build

up-app:
	docker-compose -f docker-compose-app.yml up -d
up-test:
	docker-compose -f docker-compose-test.yml up -d
up-both:
	docker-compose -f docker-compose-app.yml up -d
	docker-compose -f docker-compose-test.yml up -d

down-app:
	docker-compose -f docker-compose-app.yml down
down-test:
	docker-compose -f docker-compose-test.yml down
down-both:
	docker-compose -f docker-compose-app.yml down
	docker-compose -f docker-compose-test.yml down

show-test-logs:
	docker-compose -f docker-compose-test.yml logs -f api-test