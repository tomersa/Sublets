all: test

install: install_dependencies

install_dependencies:
	sudo ./install_dependencies.sh

test: res/input_html.html
	python src/Main.py res/encrypted_key

