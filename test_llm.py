from llm import summarize_recent_errors

fake_readings = [
    {"RH_ERROR_pred": 1.2},
    {"RH_ERROR_pred": 3.4},
    {"RH_ERROR_pred": 5.6},
    {"RH_ERROR_pred": 7.8},
]

print(summarize_recent_errors(fake_readings))
