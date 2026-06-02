# K-12 Knowledge Repository

This repository stores verified and regularly updated resources for K-12 schools, teachers, and students.

## Coverage
- Ministry of Education
- Directorate of Education
- CBSE
- NCF
- NEP
- Assessment resources
- Pedagogy resources
- Capacity building programs
- Subject-wise learning resources

## Source principles
- Prefer official government and board sources.
- Track source URLs, issue dates, review dates, and status.
- Mark items as Active, Superseded, Archived, or Pending Review.

## Update frequency
- CBSE and DoE circulars: weekly
- Ministry and NCERT updates: monthly
- Capacity building resources: weekly
- Assessment and pedagogy resources: monthly

## Folder structure
```
k12-knowledge-repository/
├─ README.md
├─ data/           # CSV repository files
├─ docs/           # Policy and taxonomy docs
├─ sources/        # Official source links
├─ scripts/        # Build and update scripts
├─ ai/             # AI layer docs and API contract
├─ src/            # React frontend source
├─ netlify/        # Netlify functions
└─ .github/        # CI/CD workflows
```

## Stakeholder views
- **Principal**: Compliance, circulars, and policy.
- **Teacher**: Pedagogy, assessment, training.
- **Student**: Subject resources and revision.
- **Parent**: Notices and academic updates.
- **Coordinator**: Source index and update logs.

## Deployment
Frontend deployed via Netlify. Data updates via GitHub Actions weekly.

## Built by
Naushad Lucky · IOE · EdTech for India
