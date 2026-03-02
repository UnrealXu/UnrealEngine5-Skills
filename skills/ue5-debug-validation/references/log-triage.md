# Log Triage Guide

## Input Sources
- `Saved/Logs/*.log`
- Unreal Output Log panel export

## Priority
1. `Error`
2. `Warning`
3. Category-specific anomalies (Blueprint, Net, Asset)

## Rule
- Capture timestamp + category + message.
- Correlate first meaningful error with user action timeline.
- Ignore repeated derivative spam after root failure is identified.
