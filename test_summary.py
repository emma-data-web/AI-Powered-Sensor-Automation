from llm import summarize_recent_errors_local

fake_readings = [
    {"RH_ERROR_pred": 1.2},
    {"RH_ERROR_pred": 2.5},
    {"RH_ERROR_pred": 4.1},
    {"RH_ERROR_pred": 6.0},
]

print(summarize_recent_errors_local(fake_readings))
