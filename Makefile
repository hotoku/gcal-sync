.PHONY: all
all:
	python -m gcal_sync credentials/gcal_sync-jdsc.json credentials/gcal_sync-hotoku.json


.PHONY: clean
clean:
	rm -f credentials/gcal_sync-jdsc-token.json credentials/gcal_sync-hotoku-token.json
