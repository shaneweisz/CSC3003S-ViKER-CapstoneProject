# Run `make run` to run the application
run:
	python3 src/main.py

# Run `make runARM n=[1 OR 2 OR 3]` to run the ARM Example
runARM:
	python3 src/arm_example.py $(n)

# Run `make runEER t=[normal OR weak]` to run the ARM Example
runEER:
	python3 src/eer_example.py $(t)

# Run `make gui` to view the static GUI of the application
gui:
	python3 src/view.py

# Run `make clean` to get rid of saved transformation outputs
clean:
	rm EER_XML_Schema/*_transformed.txt

# Run `make tests` to run all unit tests
tests:
	python3 src/eer_unit_tests.py
	python3 src/eer_constraints_unit_tests.py
	python3 src/arm_unit_tests.py
