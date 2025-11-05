"""
专项套题 Y（简易规则引擎）- 空白版

规则格式（示例）：
[
  {"when": {"field": "amount", "op": "gt", "value": 100}, "then": {"set": {"flag": "HIGH"}}},
  {"when": {"field": "amount", "op": "gte", "value": 0}, "then": {"compute_tax": {"rate": 0.13}}}
]

要求：
- 支持条件操作符：eq/ne/gt/gte/lt/lte/in
- 支持动作：set（并入字段）、compute_tax（新增 tax=round(amount*rate/(1+rate),2)）
"""

from __future__ import annotations

from typing import Any, Dict, List


def match(cond: Dict[str, Any], row: Dict[str, Any]) -> bool:
    # TODO：实现各操作符
    return False


def apply_actions(actions: Dict[str, Any], row: Dict[str, Any]) -> Dict[str, Any]:
    # TODO：实现 set 与 compute_tax
    return row


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
    print("[Y 空白版] 自检断言：全部通过（请完善实现）")


if __name__ == "__main__":
    _run_self_tests()

