FILE_PATH = ./src
TEST_PATH = ./src/tests

.PHONY: lint
lint:
	@black $(FILE_PATH)
	@isort --profile black $(FILE_PATH)
	@flake8 --max-line-length 88 --extend-ignore=E203 $(FILE_PATH)
	@bandit --exclude $(TEST_PATH) $(FILE_PATH)
