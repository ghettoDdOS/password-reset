
.PHONY: clean
clean:
	sudo rm -rf ./build
	sudo rm -rf ./dist

.PHONY: build
build:
	poetry run pyinstaller ./password_reset/main.py -F --specpath ./dist --distpath ./iso/airootfs/usr/bin/ --name password_reset
	mkdir -p ./dist/iso
	sudo mkarchiso -v -w ./build/iso -o ./dist/iso iso/

.PHONY: run
run:
	run_archiso -u -i ./dist/iso/*
