MKDIR = mkdir -p
CP = cp -r
ZIP = zip
RM = rm -rf
CD = cd

SOURCES = $(wildcard src/*.py)
ASCIIDOC_FILTER = asciidoc-filter/shaape-filter.conf
BUILD_DIR = build
.PHONY: install clean
install-filter: 
	$(RM) $(BUILD_DIR)    
	$(MKDIR) $(BUILD_DIR)
	$(CP) $(SOURCES) $(BUILD_DIR)
	$(CP) $(ASCIIDOC_FILTER) $(BUILD_DIR)
	$(CD) $(BUILD_DIR) && $(ZIP) shaape.zip ./* -r    
	-asciidoc --filter remove shaape   
	asciidoc --filter install $(BUILD_DIR)/shaape.zip   

upload-pipy: 
	python setup.py sdist upload    

clean:
	$(RM) $(BUILD_DIR)    
