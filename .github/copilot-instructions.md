**Purpose**
- **Summary:** Guidance for AI coding agents to be immediately productive in this repository.

**Big Picture**
- **Architecture:** Python project organized under `src/` with the primary package `src/DMARTProject`. Core concerns are split into `components/` (data_ingestion, data_transformation, data_validation, model_trainer, model_evaluation), `pipelines/` (training_pipeline.py, prediction_pipeline.py), `loggers/` (logger.py), and `utils/` (common helpers).
- **Data flow:** ingestion -> validation -> transformation -> training -> evaluation -> prediction. Look at `src/DMARTProject/components/*` and `src/DMARTProject/pipelines/*` to follow actual implementations.

**Key Files / Entry Points**
- **Runner / entry:** [app.py](app.py) — lightweight app bootstrap that imports the project logger and `CustomException`.
- **Pipelines:** [src/DMARTProject/pipelines/training_pipeline.py](src/DMARTProject/pipelines/training_pipeline.py) and [src/DMARTProject/pipelines/prediction_pipeline.py](src/DMARTProject/pipelines/prediction_pipeline.py).
- **Components:** examples: [src/DMARTProject/components/data_ingestion.py](src/DMARTProject/components/data_ingestion.py), [src/DMARTProject/components/data_transformation.py](src/DMARTProject/components/data_transformation.py).
- **Logging / errors:** [src/DMARTProject/loggers/logger.py](src/DMARTProject/loggers/logger.py) and top-level [exception.py](exception.py) (project wraps exceptions using `CustomException(e, sys)`).

**Developer Workflow**
- **Virtualenv:** use the included venv at `dmart_env/` on Windows: `dmart_env\\Scripts\\activate.bat` then `python -m pip install -r requirement.txt`.
- **Run:** common quick runs: `python template.py` or `python app.py` from repository root. CI workflows live in `.github/workflows/`.
- **Build / package:** packaging metadata exists in `setup.py`; built artifacts appear in `build/` and `dist/` when run.

**Project Conventions & Patterns**
- **Single package import path:** code imports use `src.DMARTProject.*`. Prefer modifying files under `src/DMARTProject` to preserve import paths.
- **Logger usage:** prefer `from src.DMARTProject.loggers.logger import logging` and use `logging.info()/error()` for runtime messages. See [app.py](app.py) for the pattern.
- **Exception wrapping:** when catching exceptions, wrap with `CustomException(e, sys)` to preserve stack and uniform error handling.
- **Pipelines composition:** pipelines import and instantiate component classes/functions rather than procedural scripts. To change data flow, edit `pipelines/*` and update component wiring in those files.

**Integrations & External Dependencies**
- **Database / SQL:** `DMART.sql` contains DB schema or sample SQL used by the project; check `components` for DB usage.
- **Third-party libs:** installed in `dmart_env/Lib/site-packages/` and listed in `requirement.txt` — consult that file when adding dependencies.

**What to change and where (examples)**
- To add a new preprocessing step: add it to `src/DMARTProject/components/data_transformation.py` and call it from `src/DMARTProject/pipelines/training_pipeline.py`.
- To change logging format: modify `src/DMARTProject/loggers/logger.py` and then search for `from src.DMARTProject.loggers.logger import logging` to confirm usages.

**Safety / gotchas discovered in repository**
- There are duplicate/variant package paths (e.g., `src/DMART Project/` with a space and `src/DMARTProject/`). Prefer `src/DMARTProject/` for imports; avoid creating modules with spaces.
- Many operations assume the venv `dmart_env/` is active — running without it may load incompatible packages.

**How to ask the maintainers (prompts for PRs)**
- Mention the pipeline and component touched (e.g., "I updated `training_pipeline.py` to add step X and updated `data_transformation.py` accordingly").
- Include a short run command (how you executed code locally) and whether `dmart_env` was active.

**If you need more context**
- Inspect these files first: [app.py](app.py), [src/DMARTProject/pipelines/training_pipeline.py](src/DMARTProject/pipelines/training_pipeline.py), [src/DMARTProject/components/data_ingestion.py](src/DMARTProject/components/data_ingestion.py), [src/DMARTProject/loggers/logger.py](src/DMARTProject/loggers/logger.py), [exception.py](exception.py).

Please review and tell me if you'd like more examples or deeper docstrings for any component.