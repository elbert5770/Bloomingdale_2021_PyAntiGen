"""Experiment registry: one entry per experiment for run and optimize."""
from .Data import load_experiment1_data
from .Events import generate_events

EXPERIMENTS = [
    {"id": "1", "event_func": generate_events, "load_data": load_experiment1_data, "label": "IV Dose 36 mg/kg"}
]
