CRED_DIR := credentials


# JDSC_CAL_ID := c_2536421556053b08bcb13599e54e80ec0e260f9a6de131d42419930bb6d0aeff@group.calendar.google.com
JDSC_CAL_ID := primary
# ME_CAL_ID := 3427b56b797a40bfe4a664440ac4116972f521d8b436fcc8c6776a2619f55e40@group.calendar.google.com
ME_CAL_ID := primary
DURATION := 2


.PHONY: all
all:
	python -m gcal_sync run \
		--duration=$(DURATION) \
		$(CRED_DIR) \
JDSC:$(JDSC_CAL_ID),\
ME:$(ME_CAL_ID)


.PHONY: credentials
credentials:
	python -m gcal_sync $(CRED_DIR) \
		$(CRED_DIR)/gcal-sync-001.json \
		$(CRED_DIR)


.PHONY: clean
clean:
	rm -f $(CRED_DIR)/*-token.json
