PLIST_NAME=info.hotoku.gce.copy-history
EXE_NAME=run
HOTOKU_PLIST_DESTPATH=$(HOME)/Library/LaunchAgents


.PHONY: all
all: load run
	@echo making $@


.PHONY: clean
clean: unload
	@echo making $@
	rm -f $(PLIST_NAME).plist run stdout stderr


.PHONY: load
load: $(PLIST_NAME).plist unload permission
	@echo making $@
	cp -f $(PLIST_NAME).plist $(HOTOKU_PLIST_DESTPATH)
	launchctl load $(HOTOKU_PLIST_DESTPATH)/$(PLIST_NAME).plist


.PHONY: unload
unload:
	@echo making $@
	launchctl unload $(HOTOKU_PLIST_DESTPATH)/$(PLIST_NAME).plist || true
	rm -f $(HOTOKU_PLIST_DESTPATH)/$(PLIST_NAME).plist


.PHONY: permission
permission: $(EXE_NAME)
	chmod 755 $(EXE_NAME)


info.hotoku.gce.copy-history.plist: info.hotoku.gce.copy-history.plist.jinja
	@echo making $@
	jinja2 -D HOTOKU_GCE_WORKDIR=$(HOTOKU_GCE_WORKDIR) $< > $@


.PHONY: $(EXE_NAME)
$(EXE_NAME): $(EXE_NAME).jinja
	@echo making $@
	jinja2 \
		-D INSTANCE_NAME=$(INSTANCE_NAME) \
		-D INSTANCE_PROJECT=$(INSTANCE_PROJECT) \
		-D PYTHON_GCE_ZONE=$(PYTHON_GCE_ZONE) \
		-D GOOGLE_USER=$(GOOGLE_USER) \
		$< > $@
