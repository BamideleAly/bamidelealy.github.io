.PHONY: quality test inventory serve print-report

quality:
	python3 tools/quality-check.py
	node --check script.js
	node --check script.min.js

test:
	python3 -m unittest discover -s tests -p 'test_*.py'

inventory:
	python3 tools/site-inventory.py

serve:
	python3 tools/serve-with-headers.py --port 8081

print-report:
	python3 tools/export-print-pdf.py http://127.0.0.1:8081/notes/commercialising-quantum-global-2026.html /tmp/cqg-overview-print.pdf
