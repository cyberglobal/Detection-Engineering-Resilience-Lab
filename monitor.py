#!/usr/bin/env python3

import json
import sys
from pathlib import Path

# My 4625 events did not give me a useful TargetUserName field in Splunk.
# Account_Name was multi-value instead, with labuser as the failed account.
needed_fields = ["Account_Name", "Source_Network_Address"]


def load_sample(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_health(data):
    # Tier 1: did the synthetic heartbeat make it through the forwarding pipeline?
    heartbeat = data.get("heartbeat", {})
    pipeline_ok = heartbeat.get("received", False)

    if not pipeline_ok:
        return {
            "pipeline": "DEGRADED",
            "telemetry": "UNKNOWN",
            "detection": "UNRELIABLE",
            "reason": "Heartbeat missing - forwarding pipeline may be down"
        }

    # Tier 2: does the 4625 event still contain the fields my rule depends on?
    event = data.get("bruteforce_event", {})
    missing_fields = []

    for field in needed_fields:
        value = event.get(field)

        if isinstance(value, list):
            if not any(str(item).strip() for item in value):
                missing_fields.append(field)
        elif value is None or str(value).strip() == "":
            missing_fields.append(field)

    if missing_fields:
        return {
            "pipeline": "HEALTHY",
            "telemetry": "DEGRADED",
            "detection": "UNRELIABLE",
            "reason": "Missing field(s): " + ", ".join(missing_fields)
        }

    return {
        "pipeline": "HEALTHY",
        "telemetry": "HEALTHY",
        "detection": "RELIABLE",
        "reason": "Heartbeat arrived and the required 4625 fields are present"
    }


def print_report(result, sample_name):
    print("=" * 58)
    print("DETECTION HEALTH REPORT")
    print("=" * 58)
    print("Sample:", sample_name)
    print()
    print("Pipeline:", result["pipeline"])
    print("Brute-force telemetry:", result["telemetry"])
    print("Brute-force detection:", result["detection"])
    print("Reason:", result["reason"])
    print("=" * 58)


def main():
    if len(sys.argv) != 2:
        print("Usage: python monitor.py sample-data/healthy-real.json")
        return

    sample_path = Path(sys.argv[1])

    if not sample_path.exists():
        print("File not found:", sample_path)
        return

    data = load_sample(sample_path)
    result = check_health(data)
    print_report(result, sample_path.name)


if __name__ == "__main__":
    main()
