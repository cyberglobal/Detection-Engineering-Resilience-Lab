# Detection Engineering & Resilience Lab

A Windows and Splunk SOC lab focused on brute-force detection and detection reliability.

## Overview

The lab detects repeated failed Windows logons and checks whether the detection can still be trusted.

The health monitor checks two things:

- **Tier 1 - Pipeline health:** checks whether a synthetic heartbeat reaches Splunk.
- **Tier 2 - Telemetry health:** checks whether the required Windows Event ID 4625 fields are still present.

The monitor reports whether the detection is **RELIABLE** or **UNRELIABLE**, along with the reason.

## Run the Health Monitor

Python 3 is required.

From the repository folder, run:

```bash
python monitor.py sample-data/healthy-real.json
```

Other test states:

```bash
python monitor.py sample-data/pipeline-degraded.json
python monitor.py sample-data/schema-degraded.json
python monitor.py sample-data/recovered.json
```

## Test States

- `healthy-real.json` - pipeline and required telemetry are healthy
- `pipeline-degraded.json` - heartbeat is missing
- `schema-degraded.json` - controlled simulation of a missing required field
- `recovered.json` - pipeline has returned to a healthy state

## Project Report

See `Detection_Engineering_Resilience_Lab.pdf` for the full project methodology, testing and results.

