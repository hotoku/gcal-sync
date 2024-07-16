# JDSC_CAL_ID := c_4c069b0468419e2aa0ead1d9fef823021cf4f406d81f84ea931f121481cb38c1@group.calendar.google.com
# ME_CAL_ID := a6d4b4d0b6d994a56a9b23e5a30e7d1fd12dcace3f3899a03be768f4894a1be1@group.calendar.google.com
# INCTORE_CAL_ID := c_83968eb2553fe7c812e95f2ab335b496965c76a984471d7ce72008e33199551d@group.calendar.google.com
JDSC_CAL_ID := primary
ME_CAL_ID := primary
INCTORE_CAL_ID := primary
MELLON_CAL_ID := primary


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
MELLON:$(MELLON_CAL_ID):google


.PHONY: clear
clear:
	python -m gcal_sync clear \
		--duration=$(DURATION) \
		$(CRED_DIR) \
ME:$(ME_CAL_ID):google,\
JDSC:$(JDSC_CAL_ID):google,\
INCTORE:$(INCTORE_CAL_ID):google,\
MELLON:$(MELLON_CAL_ID):google


.PHONY: credentials
credentials:
	python -m gcal_sync $@ \
		$(CRED_DIR)/gcal-sync-001.json \
		$(CRED_DIR) \
		JDSC:google,ME:google,INCTORE:google,MELLON:google


.PHONY: clean
clean:
	rm -f $(CRED_DIR)/*-token.json
