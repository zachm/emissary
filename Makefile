

# port on server to forward to docker.
PORT=8080

.PHONY: build run test all

test:
	docker build -t emissary_test -f Dockerfile-test .
	docker run emissary_test


debug_build:
	docker build -t emissary_skeleton -f Dockerfile-skeleton .

debug: debug_build
	docker run -it -p $(PORT):8008 -v $(shell pwd):/code:rw emissary_skeleton


build:
	docker build -t emissary .

run: build
	# -it keeps everything in the foreground; Ctrl+C to kill.
	docker run -it -p $(PORT):8008 emissary
