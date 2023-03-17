CRED_DIR := credentials


# JDSC_CAL_ID := c_4c069b0468419e2aa0ead1d9fef823021cf4f406d81f84ea931f121481cb38c1@group.calendar.google.com
JDSC_CAL_ID := primary
# ME_CAL_ID := a6d4b4d0b6d994a56a9b23e5a30e7d1fd12dcace3f3899a03be768f4894a1be1@group.calendar.google.com
ME_CAL_ID := primary
ATTTA_CAL_ID := primary
INCTORE_CAL_ID := primary


DURATION := 60


.PHONY: all
all:
	python -m gcal_sync run \
		--duration=$(DURATION) \
		$(CRED_DIR) \
ME:$(ME_CAL_ID),\
JDSC:$(JDSC_CAL_ID),\
ATTTA:$(ATTTA_CAL_ID),\
INCTORE:$(INCTORE_CAL_ID)


.PHONY: clear
clear:
	python -m gcal_sync clear \
		--duration=$(DURATION) \
		$(CRED_DIR) \
ME:$(ME_CAL_ID),\
JDSC:$(JDSC_CAL_ID),\
ATTTA:$(ATTTA_CAL_ID),\
INCTORE:$(INCTORE_CAL_ID)


.PHONY: credentials
credentials:
	python -m gcal_sync $(CRED_DIR) \
		$(CRED_DIR)/gcal-sync-001.json \
		$(CRED_DIR) \
		JDSC,ME,ATTTA,INCTORE


.PHONY: clean
clean:
	rm -f $(CRED_DIR)/*-token.json
