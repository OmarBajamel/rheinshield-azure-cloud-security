PYTHON ?= python

.PHONY: bootstrap demo validate test screenshots release-check clean azure-preflight azure-plan azure-deploy evidence azure-destroy-plan azure-destroy-execute
bootstrap:
	npm ci
	$(PYTHON) -m pip install -e ".[dev]"
	docker version

demo:
	$(PYTHON) tools/synthetic-telemetry/generate.py
	npm run dev

validate:
	npm run typecheck
	npm run lint
	$(PYTHON) tools/detection-test-harness/validate.py
	$(PYTHON) tools/sanitization/scan_public.py

test: validate
	npm test
	$(PYTHON) -m pytest -q
	npm run build

screenshots:
	npm run build
	npm run screenshots

release-check:
	npm run release:check
	$(PYTHON) tools/release/build_release.py
	$(PYTHON) tools/sanitization/scan_public.py
	$(PYTHON) tools/evidence-collector/collect.py

clean:
	$(PYTHON) tools/project-clean/clean.py

azure-preflight:
	powershell -NoProfile -File scripts/azure-preflight.ps1
azure-plan:
	powershell -NoProfile -File scripts/deploy-lab.ps1 -PlanOnly
azure-deploy:
	powershell -NoProfile -File scripts/deploy-lab.ps1
evidence:
	powershell -NoProfile -File scripts/capture-evidence.ps1
azure-destroy-plan:
	powershell -NoProfile -File scripts/destroy-lab.ps1 -Suffix $(SUFFIX)
azure-destroy-execute:
	powershell -NoProfile -File scripts/destroy-lab.ps1 -Suffix $(SUFFIX) -Execute
