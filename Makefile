JDSC_CAL_ID := primary
ME_CAL_ID := primary
INCTORE_CAL_ID := primary
ATTTA_CAL_ID := primary
JFR_CAL_ID := primary


CRED_DIR := credentials


DURATION := 120


.PHONY: all
all:
	python -m gcal_sync run \
		--duration=$(DURATION) \
		$(CRED_DIR) \
ME:$(ME_CAL_ID):google,\
JDSC:$(JDSC_CAL_ID):google,\
INCTORE:$(INCTORE_CAL_ID):google,\
ATTTA:$(ATTTA_CAL_ID):google,\
JFR:$(JFR_CAL_ID):google


.PHONY: clear
clear:
	python -m gcal_sync clear \
		--duration=$(DURATION) \
		$(CRED_DIR) \
ME:$(ME_CAL_ID):google,\
JDSC:$(JDSC_CAL_ID):google,\
INCTORE:$(INCTORE_CAL_ID):google,\
ATTTA:$(ATTTA_CAL_ID):google,\
JFR:$(JFR_CAL_ID):google


.PHONY: credentials
credentials:
	python -m gcal_sync $(CRED_DIR) \
		$(CRED_DIR)/gcal-sync-001.json \
		$(CRED_DIR) \
		JDSC:google,ME:google,INCTORE:google,ATTTA:google,JFR:google


.PHONY: clean
clean:
	rm -f $(CRED_DIR)/*-token.json
