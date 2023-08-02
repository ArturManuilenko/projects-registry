SHELL := /bin/bash
CWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ME := $(shell whoami)

docker_login_unic_lab:
	docker login gitlab.neroelectronics.by:5050 -u unic_lab_developers -p Vw3o4gBzgH_GGUzFs7NM

.PHONY:check_env

check_env:
	@./srv/check_env.sh

cleanup:
	@# git submodule foreach "git fetch && git merge origin/dev"
	pipenv update

	# pre-commit
	cp -f "${CWD}/srv/git.hook.pre-commit.sh" "${CWD}/.git/hooks/pre-commit"
	chmod +x "${CWD}/.git/hooks/pre-commit"

	# pre-push
	cp -f "${CWD}/srv/git.hook.pre-push.sh" "${CWD}/.git/hooks/pre-push"
	chmod +x "${CWD}/.git/hooks/pre-push"

up:
	docker-compose up --remove-orphans --build  \
		service__api \
		service__communication__balancer \
		service__common__db \

down:
	docker-compose down -v

fix_own:
	@echo "me: $(ME)"
	sudo chown $(ME):$(ME) -R .

lint:
	./src/bin-lint.sh

tests:
	./src/bin-tests.sh

######################## MANAGER SERVICE DB START ########################

manager__common__db__migrations:
	docker-compose run --rm manager__common__db /docker_app/src/manager__common__db/bin-migrate.sh --migrate

manager__common__db__revision:
	docker-compose run --rm manager__common__db /docker_app/src/manager__common__db/bin-migrate.sh --revision

manager__common__db__init:
	docker-compose run --rm manager__common__db /docker_app/src/manager__common__db/bin-migrate.sh --init

manager__common__db__upgrade:
	docker-compose run --rm manager__common__db /docker_app/src/manager__common__db/bin-migrate.sh --upgrade

manager__common__db__downgrade:
	docker-compose run --rm manager__common__db /docker_app/src/manager__common__db/bin-migrate.sh --downgrade

########################  MANAGER SERVICE DB END ########################
