# ClauseCraft (v0.1)

A tiny legal-tech helper that

1. Converts **PDF / DOCX / TXT** contracts into plain text.
2. Flags selected clauses (e.g. *confidentiality*, *termination*) with simple regex rules.
3. Prints a short snippet for each hit and saves an optional full-text copy.

---

## Quick-start

```powershell
# create & activate a virtual environment
python -m venv .venv
. .venv\Scripts\Activate.ps1      # Windows PowerShell

# install dependencies
pip install -r requirements.txt

# run on the demo contract
python clausecraft_extract.py sample.pdf --clauses termination confidentiality
