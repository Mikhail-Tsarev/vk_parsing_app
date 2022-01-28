# https://docs.docker.com/engine/reference/run/

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

include $(ROOT_DIR)/app/.env

.PHONY: help dependencies up start stop restart status ps clean
.DEFAULT_GOAL:=help

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

