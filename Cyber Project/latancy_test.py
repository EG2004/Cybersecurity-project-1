import time
from detector import rule_based_detection
from ml_model import ml_detection

test_inputs = [
    "admin",
    "hello123",
    "normalUser",
    "' OR 1=1 --",
    "UNION SELECT username, password FROM users",
    "'; DROP TABLE users; --",
    "SeLeCt * FROM users",
    "john_doe",
    "' OR 'a'='a",
    "guest123"
]

# Rule-based latency
rule_times = []
for test_input in test_inputs:
    start = time.perf_counter()
    rule_based_detection(test_input)
    end = time.perf_counter()
    rule_times.append(end - start)

# ML latency
ml_times = []
for test_input in test_inputs:
    start = time.perf_counter()
    ml_detection(test_input)
    end = time.perf_counter()
    ml_times.append(end - start)

avg_rule_latency = sum(rule_times) / len(rule_times)
avg_ml_latency = sum(ml_times) / len(ml_times)

print("Average Rule-Based Latency:", avg_rule_latency, "seconds")
print("Average ML Latency:", avg_ml_latency, "seconds")