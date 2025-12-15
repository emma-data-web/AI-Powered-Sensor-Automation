from llm import build_summary_prompt

fake_readings = [
    {"RH_ERROR_pred": 1.2},
    {"RH_ERROR_pred": 2.5},
    {"RH_ERROR_pred": 4.1},
    {"RH_ERROR_pred": 6.0},
]

prompt = build_summary_prompt(fake_readings)
print(prompt)
