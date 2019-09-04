# Run `make run` to run the application
run:
	python3 src/main.py

# Run `make tests` to run all unit tests
tests:
	python3 src/unit_tests_eer.py
	python3 src/unit_tests_constraints.py
	python3 src/unit_tests_arm.py

# Run `make clean` to get rid of saved transformation outputs
clean:
	rm Transformation_Outputs/*.txt
	rm *.txt

# Run `make gui` to view the static GUI of the application
gui:
	python3 src/view.py
