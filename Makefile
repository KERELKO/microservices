PRODUCT = product-app
AUTH = auth-app

.PHONY: up
up:
	./entrypoint.sh

.PHONY: auth-logs
auth-logs:
	docker logs ${AUTH}

.PHONY: product-logs
product-logs:
	docker logs ${PRODUCT}
