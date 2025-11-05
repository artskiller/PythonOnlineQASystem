"""
专项套题 Y（简易规则引擎）- 答案版
"""

from __future__ import annotations

from typing import Any, Dict, List


def match(cond: Dict[str, Any], row: Dict[str, Any]) -> bool:
    f = cond.get("field")
    op = cond.get("op")
    val = cond.get("value")
    x = row.get(f)
    if op == "eq":
        return x == val
    if op == "ne":
        return x != val
    if op == "gt":
        return x > val
    if op == "gte":
        return x >= val
    if op == "lt":
        return x < val
    if op == "lte":
        return x <= val
    if op == "in":
        return x in (val or [])
    return False


def apply_actions(actions: Dict[str, Any], row: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(row)
    if "set" in actions:
        out.update(actions["set"] or {})
    if "compute_tax" in actions:
        rate = float(actions["compute_tax"].get("rate", 0))
        amt = float(out.get("amount", 0))
        net = amt / (1 + rate)
        out["tax"] = round(amt - net, 2)
    return out


def apply_rules(row: Dict[str, Any], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    out = dict(row)
    for r in rules:
        if match(r.get("when", {}), out):
            out = apply_actions(r.get("then", {}), out)
    return out


def _run_self_tests():
    rules = [
        {"when": {"field": "amount", "op": "gt", "value": 100}, "then": {"set": {"flag": "HIGH"}}},
        {"when": {"field": "amount", "op": "gte", "value": 0}, "then": {"compute_tax": {"rate": 0.13}}},
    ]
    r = apply_rules({"amount": 113}, rules)
    assert r["flag"] == "HIGH" and round(r["tax"], 2) == 13.0
    print("[Y 答案版] 自检断言：全部通过")


if __name__ == "__main__":
    _run_self_tests()

