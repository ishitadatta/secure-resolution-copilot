from pathlib import Path
import json

from fastapi import APIRouter

from ..services.triage import classify_incident

router = APIRouter(prefix="/evals", tags=["evals"])


@router.post("/run")
def run_eval() -> dict[str, object]:
    local_path = Path(__file__).resolve().parents[4] / "evals" / "scenarios.json"
    container_path = Path("/evals/scenarios.json")
    scenarios_path = local_path if local_path.exists() else container_path
    scenarios = json.loads(scenarios_path.read_text())

    total = len(scenarios)
    passed = 0
    details: list[dict[str, object]] = []

    for scenario in scenarios:
        triage = classify_incident(scenario["message"])
        ok = triage.incident_type == scenario["expected_incident_type"] and triage.severity in scenario["acceptable_severity"]
        if ok:
            passed += 1
        details.append(
            {
                "id": scenario["id"],
                "expected_incident_type": scenario["expected_incident_type"],
                "predicted_incident_type": triage.incident_type,
                "predicted_severity": triage.severity,
                "pass": ok,
            }
        )

    return {
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "details": details,
    }
