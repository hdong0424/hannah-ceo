# Use a Landing Page as the Repository Entrance

**Date:** 2026-08-16  
**Status:** Accepted

## Question

How should the `hannah-ceo` repository relate to Hannah's proposed biographical and career landing page?

## Options considered

### A. Add the landing page to `hannah-ceo`

Keep the repository as an entrepreneurship and coding journal while using a simple landing page as its public entrance.

### B. Use a separate repository

Keep `hannah-ceo` documentation-only and build the landing page as an independent project.

### C. Postpone the landing page

Focus only on Vlog IP business records before creating a technical artifact.

## Decision

Hannah chose option A.

The `hannah-ceo` repository will remain a record of entrepreneurship, projects, coding, decisions, and lessons. A simple landing page will become the public entrance to that work.

## Reasoning

- The repository already contains the beginnings of Hannah's current professional and entrepreneurial story.
- A landing page can help an unfamiliar visitor understand the repository and find its most important work.
- Building it here creates a small, real technical artifact instead of adding more organizational infrastructure.
- Starting with plain HTML and CSS will help Hannah rebuild core skills and understand the implementation before choosing a framework.

## Consequences

- The first technical files will be `index.html` and `styles.css`.
- The first version will not require a JavaScript framework, database, authentication, or AI feature.
- Public biographical and professional claims require Hannah's review and approval.
- Deployment remains a separate future decision.
- The Vlog IP project and journal records remain part of the repository rather than being replaced by the landing page.

## Still undecided

- The landing page's exact sections and wording
- Visual direction and branding
- Whether and where the site will be deployed
- The first AI prototype and its relationship to the landing page

## Revisit this decision if

- The landing page grows into an application with substantially different technical needs.
- The repository becomes difficult for visitors or Hannah to navigate.
- A separate product identity or deployment process makes an independent repository more appropriate.
