all: clean test

clean:
	rm -rf output/

install: install_dependencies

install_dependencies:
	sudo ./install_dependencies.sh

test: 
	python src/Main.py res/sublet_in_telaviv_for_short_periods
 

