# Brand Kit Workflow

## Intent Interpretation

Users often describe a brand in fragments: a name, a material metaphor, a mood, a philosophical story, a cultural platform, or a disliked old logo. Treat these as constraints for a system, not as a prompt dump.

The useful abstraction is “water shape”:

- flow into the repo's existing structure before deciding output paths;
- flow into the product's actual surfaces before deciding asset formats;
- flow into the user's cultural/philosophical language before deciding style;
- then harden into a stable VI, DAG, asset manifest, and production files.

## Decision Gates

1. **Current-state gate**
   - What asset files already exist?
   - Which files are source masters versus generated outputs?
   - Which commands regenerate outputs?
   - Which docs/configs/components mention old brand names?

2. **Target-structure gate**
   - What is the canonical brand directory?
   - Where do approved masters live?
   - Where do generated candidates live?
   - Which files are safe to delete as rejected/legacy?

3. **VI gate**
   - What is the brand idea in one sentence?
   - What is the shape grammar?
   - What materials and palette are allowed?
   - What cultural tone should it carry?
   - What negative readings must be avoided?

4. **DAG gate**
   - Which assets must be generated before later assets can use them as references?
   - Which assets require consistency versus variety?
   - Which outputs are exploratory and which are production?

5. **Consumption gate**
   - Which product files must change?
   - Which generated outputs must be rebuilt?
   - Which platform constraints apply?

6. **Hygiene gate**
   - Are rejected assets gone?
   - Are old names/remotes/docs removed or intentionally preserved?
   - Are tests, build scripts, and visual checks complete?

## Deliverable Shape

A strong brand-kit pass usually creates or updates:

- visual identity doc;
- asset inventory and migration checklist;
- generation DAG/prompt file;
- approved masters directory;
- generated candidate/output directory;
- processed/exported production assets;
- code/config integrations;
- verification notes.

Keep documents factual enough for future agents to continue the work without asking why a visual decision was made.
