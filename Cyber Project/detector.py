import re


def rule_based_detection(user_input):
    text = user_input.strip()
    text_lower = text.lower()

    reasons = []

    # 1. Classic SQL injection keywords
    sql_keywords = [
        "select", "union", "drop", "insert", "delete", "update",
        "where", "from", "table", "database", "alter", "exec"
    ]

    for keyword in sql_keywords:
        if keyword in text_lower:
            reasons.append(f"SQL keyword: {keyword}")

    # 2. Logical operator abuse
    if re.search(r"\bor\b", text_lower):
        reasons.append("Logical operator: OR")

    if re.search(r"\band\b", text_lower):
        reasons.append("Logical operator: AND")

    # 3. Always-true conditions
    always_true_patterns = [
        r"1\s*=\s*1",
        r"'a'\s*=\s*'a'",
        r'"a"\s*=\s*"a"',
        r"'1'\s*=\s*'1'"
    ]

    for pattern in always_true_patterns:
        if re.search(pattern, text_lower):
            reasons.append("Always-true condition")
            break

    # 4. Comment symbols
    if "--" in text or "#" in text or "/*" in text or "*/" in text:
        reasons.append("SQL comment detected")

    # 5. Dangerous punctuation / separators
    if ";" in text:
        reasons.append("Semicolon detected")

    if "'" in text:
        reasons.append("Single quote detected")

    if '"' in text:
        reasons.append("Double quote detected")

    # 6. Encoded / obfuscated attack characters
    encoded_patterns = [
        r"%27",   # '
        r"%22",   # "
        r"%3d",   # =
        r"%2d%2d" # --
    ]

    for pattern in encoded_patterns:
        if re.search(pattern, text_lower):
            reasons.append("Encoded SQL characters detected")
            break

    # 7. Suspicious function usage
    suspicious_functions = [
        "sleep", "benchmark", "concat", "substring", "ascii", "char"
    ]

    for func in suspicious_functions:
        if func in text_lower:
            reasons.append(f"Suspicious function: {func}")

    # 8. Mixed uppercase/lowercase in suspicious SQL words
    suspicious_words = [
        "select", "union", "drop", "or", "and", "insert", "delete", "update"
    ]

    for word in suspicious_words:
        if word in text_lower and any(c.islower() for c in text) and any(c.isupper() for c in text):
            reasons.append("Mixed-case suspicious input")
            break

    # 9. Too many symbols can be suspicious
    symbol_count = len(re.findall(r"['\";#=\-/*()%]", text))
    if symbol_count >= 3:
        reasons.append("High symbol count")

    # Final result
    if reasons:
        unique_reasons = list(dict.fromkeys(reasons))
        return f"🚨 Rule-Based: SQL Injection Suspected ({', '.join(unique_reasons)})"

    return "✅ Rule-Based: Input Looks Safe"
