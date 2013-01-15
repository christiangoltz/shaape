MKDIR = mkdir -p
CP = cp -r
ZIP = zip
RM = rm -rf
CD = cd

TEST_BIN = nosetests
TEST_OPTS = --with-coverage --cover-package=shaape --cover-branches --cover-html
TEST_DIR = shaape/tests

DOC_BIN = epydoc
DOC_OPTS = --graph all

SOURCES = $(wildcard shaape/*.py)
ASCIIDOC_FILTER = asciidoc-filter/shaape-filter.conf
BUILD_DIR = build
.PHONY: install install-filter clean doc tests
install-filter: 
	$(RM) $(BUILD_DIR)    
	$(MKDIR) $(BUILD_DIR)
	$(CP) $(SOURCES) $(BUILD_DIR)
	$(CP) $(ASCIIDOC_FILTER) $(BUILD_DIR)
	$(CD) $(BUILD_DIR) && $(ZIP) shaape.zip ./* -r    
	-asciidoc --filter remove shaape   
	asciidoc --filter install $(BUILD_DIR)/shaape.zip   

readme: install-filter README
	asciidoc -a data-uri README
tests:
	$(TEST_BIN) $(TEST_OPTS) $(TEST_DIR)

doc:
	$(DOC_BIN) $(DOC_OPTS) $(SOURCES)

upload-pipy: 
	python setup.py sdist upload    

clean:
	$(RM) $(BUILD_DIR)    
	$(RM) shaape/*.pyc shaape/tests/*.pyc
	$(RM) cover .coverage
	$(RM) html
	$(RM) shaape/tests/generated_images/*
	$(RM) shaape/tests/input/empty.shaape.png
