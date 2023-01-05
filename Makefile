.PHONY: all
all:
	python -m gcal_sync run \
		credentials/gcal-sync-001.json \
		primary \
		3427b56b797a40bfe4a664440ac4116972f521d8b436fcc8c6776a2619f55e40@group.calendar.google.com


.PHONY: credentials
credentials:
	python -m gcal_sync credentials \
		credentials/gcal-sync-001.json \
		credentials


.PHONY: clean
clean:
	rm -f \
		credentials/gcal_sync-jdsc-token.json \
		credentials/gcal_sync-hotoku-token.json
