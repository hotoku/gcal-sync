.PHONY: all
all:
	python -m gcal_sync \
		credentials/gcal_sync-jdsc.json \
		credentials/gcal_sync-hotoku.json \
		primary \
		3427b56b797a40bfe4a664440ac4116972f521d8b436fcc8c6776a2619f55e40@group.calendar.google.com


.PHONY: clean
clean:
	rm -f \
		credentials/gcal_sync-jdsc-token.json \
		credentials/gcal_sync-hotoku-token.json
