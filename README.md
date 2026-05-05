# postmortem-automation

Blameless postmortem automation toolkit for SRE teams.
Generates structured postmortem documents, tracks DORA metrics,
and identifies recurring incidents for automation.
Built from real postmortem practice at Southwest Airlines and Cognizant.

## What this solves
- Structured blameless postmortem generation from incident data
- DORA metrics tracking across all incidents
- Identifies recurring incidents that should be automated
- Follow-up action item tracking
- Systematic reliability improvement over time

## Scripts

| Script | What it does |
|---|---|
| `postmortem_generator.py` | Generates structured blameless postmortem documents |
| `incident_tracker.py` | Tracks incidents, DORA metrics, and recurring patterns |

## Usage

```bash
# Generate a postmortem
python postmortem_generator.py --incident INC-1234 --title "Payment API Outage" --severity P1 --duration 45

# List all postmortems
python postmortem_generator.py --list

# Add an incident to tracker
python incident_tracker.py --add --incident INC-1234 --severity P1 --mttr 45 --service payment-api --root-cause "memory-leak"

# View DORA metrics report
python incident_tracker.py --report

# Find recurring incidents to automate
python incident_tracker.py --recurring
```

## Related resume projects
- Project PulseEngine — blameless postmortems at Southwest Airlines
- ReliabilityCore — postmortem practice at Cognizant
- AlertStack — runbook library at Spring Info Tech
