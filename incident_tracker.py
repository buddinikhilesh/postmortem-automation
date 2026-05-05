#!/usr/bin/env python3
"""
incident_tracker.py
Tracks incidents, DORA metrics, and follow-up action completion.
Identifies recurring incidents and flags them for automation.

Usage:
    python incident_tracker.py --add --incident INC-1234 --severity P1 --mttr 45
    python incident_tracker.py --report
    python incident_tracker.py --recurring
"""

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from collections import Counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

DATA_FILE = "incidents.json"


class IncidentTracker:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = Path(data_file)
        self.incidents = self.load()

    def load(self) -> list:
        if self.data_file.exists():
            with open(self.data_file) as f:
                return json.load(f)
        return []

    def save(self) -> None:
        with open(self.data_file, "w") as f:
            json.dump(self.incidents, f, indent=2)

    def add(self, incident_id: str, severity: str, mttr_minutes: int,
            service: str, root_cause: str) -> None:
        incident = {
            "incident_id": incident_id,
            "severity": severity,
            "mttr_minutes": mttr_minutes,
            "service": service,
            "root_cause": root_cause,
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "automated": False,
        }
        self.incidents.append(incident)
        self.save()
        logger.info(f"Incident added: {incident_id}")

    def report(self) -> None:
        if not self.incidents:
            print("No incidents recorded")
            return

        total      = len(self.incidents)
        p1_count   = sum(1 for i in self.incidents if i["severity"] == "P1")
        p2_count   = sum(1 for i in self.incidents if i["severity"] == "P2")
        avg_mttr   = sum(i["mttr_minutes"] for i in self.incidents) / total
        automated  = sum(1 for i in self.incidents if i.get("automated"))

        print(f"\n{'='*55}")
        print(f"INCIDENT REPORT — DORA METRICS")
        print(f"{'='*55}")
        print(f"  Total incidents:     {total}")
        print(f"  P1 incidents:        {p1_count}")
        print(f"  P2 incidents:        {p2_count}")
        print(f"  Average MTTR:        {avg_mttr:.1f} minutes")
        print(f"  Automated:           {automated} ({automated/total*100:.0f}%)")
        print(f"{'='*55}\n")

    def find_recurring(self, threshold: int = 2) -> None:
        root_causes = Counter(i["root_cause"] for i in self.incidents)
        recurring = {rc: count for rc, count in root_causes.items() if count >= threshold}

        if not recurring:
            print("No recurring incidents found")
            return

        print(f"\n{'='*55}")
        print(f"RECURRING INCIDENTS — AUTOMATE THESE")
        print(f"{'='*55}")
        for root_cause, count in sorted(recurring.items(), key=lambda x: -x[1]):
            print(f"  {count}x — {root_cause}")
        print(f"\n  These should be converted to automated remediations")
        print(f"  See incident_remediator.py in sre-observability-toolkit")
        print(f"{'='*55}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track incidents and DORA metrics")
    parser.add_argument("--add", action="store_true")
    parser.add_argument("--incident", help="Incident ID")
    parser.add_argument("--severity", default="P2", choices=["P1", "P2", "P3"])
    parser.add_argument("--mttr", type=int, default=60, help="MTTR in minutes")
    parser.add_argument("--service", default="unknown")
    parser.add_argument("--root-cause", default="unknown")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--recurring", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    tracker = IncidentTracker()

    if args.add:
        if not args.incident:
            print("Provide --incident ID")
            return
        tracker.add(
            incident_id=args.incident,
            severity=args.severity,
            mttr_minutes=args.mttr,
            service=args.service,
            root_cause=args.root_cause,
        )
    elif args.report:
        tracker.report()
    elif args.recurring:
        tracker.find_recurring()
    else:
        tracker.report()


if __name__ == "__main__":
    main()
