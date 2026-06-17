# Stakeholder Packs — NotebookLM Upload Bundles

Each `.md` file in this folder is a self-contained knowledge pack for one stakeholder role.
A coordinator can download the relevant file and upload it directly to the corresponding
NotebookLM notebook without needing to know the repository folder structure.

## Files

| File | Role | NotebookLM Notebook |
|---|---|---|
| `principal-pack.md` | School Principal | Principal Notebook |
| `teacher-pack.md` | Teacher | Teacher Notebook |
| `student-pack.md` | Student | Student Notebook |
| `parent-pack.md` | Parent / Guardian | Parent Notebook |
| `coordinator-pack.md` | Knowledge Coordinator | Coordinator Notebook |
| `master-pack.md` | All stakeholders | Master / Admin Notebook |

## Update cadence

These files are regenerated automatically by `weekly-update.yml` every Monday.
Do not edit them manually — edit the source CSVs in `data/` instead.

## How to upload to NotebookLM

1. Go to [notebooklm.google.com](https://notebooklm.google.com)
2. Open the correct notebook for the role
3. Click **+ Add source** → **Upload file**
4. Select the `.md` file for that role
5. Replace the previous week's version if prompted
