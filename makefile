all: install_dependencies test

install_dependencies:
	sudo ./install_dependencies.sh

test: res/input_html.html
	python src/Main.py res/input_html.html

