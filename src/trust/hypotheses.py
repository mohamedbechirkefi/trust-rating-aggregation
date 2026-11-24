# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Frozen confirmatory analysis (protocol sections 4, 6, 8 and 13.2; EXP-001 to EXP-003 protocols).

Written at M3 before any confirmatory output existed (decision D-011). It only combines the
statistics of trust.analysis into the frozen decision rules. Where the frozen text leaves a detail
open, the choice is fixed here and recorded in D-011, never chosen after seeing results:

- Holm family p-values (EXP-001 secondary family; EXP-002 lambda and gamma contrasts): the protocol
  names Holm but not the p-value. We use the bootstrap p-value of the same stratified bootstrap
  that gives the intervals: one-sided p = (1 + #{boot <= 0}) / (B + 1) for directional contrasts,
  two-sided p = min(1, 2 * min of the two tails) for nondirectional ones. alpha = 0.05.
- H1b enters the Holm family through the contrast mean over sigma of E[D | nu=3] - E[D | nu=30]
  (one-sided, > 0); its verdict uses the frozen ordering and overlap criteria.
- EXP-003 S1 and S2 compare with the sign of the EXP-001 point estimate of Dbar; S3 counts signs
  over the 12 EXP-002 cells (lambda = 0 cells included, where both truths coincide).
"""

from __future__ import annotations

import math

import numpy as np

from trust.analysis import BOOTSTRAP_SEED, N_BOOT, paired_differences, pooled_by_level, pooled_stratified, summarise_diffs

ALPHA = 0.05


def _boot_linear(arrays: list[np.ndarray], weights: list[float], n_boot: int = N_BOOT,
                 seed: int = BOOTSTRAP_SEED) -> tuple[float, np.ndarray]:
    """Point estimate and bootstrap distribution of sum_j w_j * mean(arrays[j]), with seeds
    resampled independently within each array (stratified bootstrap)."""
    rng = np.random.default_rng(seed)
    acc = np.zeros(n_boot)
    est = 0.0
    for a, w in zip(arrays, weights):
        if a.size == 0:
            raise ValueError("empty stratum")
        est += w * float(a.mean())
        acc += w * a[rng.integers(0, a.size, size=(n_boot, a.size))].mean(axis=1)
    return est, acc


def p_one_sided_greater(boots: np.ndarray) -> float:
    return float((1 + np.sum(boots <= 0)) / (boots.size + 1))


def p_two_sided(boots: np.ndarray) -> float:
    lo = (1 + np.sum(boots <= 0)) / (boots.size + 1)
    hi = (1 + np.sum(boots >= 0)) / (boots.size + 1)
    return float(min(1.0, 2 * min(lo, hi)))


def holm(pvals: dict[str, float], alpha: float = ALPHA) -> dict[str, dict]:
    """Holm step-down: adjusted p-values and rejection decisions."""
    order = sorted(pvals, key=lambda k: (pvals[k], k))
    m = len(order)
    out, running, stop = {}, 0.0, False
    for i, k in enumerate(order):
        adj = min(1.0, (m - i) * pvals[k])
        running = max(running, adj)
        reject = (not stop) and pvals[k] <= alpha / (m - i)
        if not reject:
            stop = True
        out[k] = {"p": pvals[k], "p_holm": running, "reject": reject}
    return out


def _interval(boots: np.ndarray, est: float) -> dict:
    lo, hi, low1 = (float(x) for x in np.quantile(boots, [0.025, 0.975, 0.05]))
    return {"estimate": est, "lo95": lo, "hi95": hi, "lower_one_sided_95": low1}


def _cells_by(doc: dict) -> dict[tuple, str]:
    """Map from the tuple of grid values (in key order) to cell id."""
    return {tuple(repr(v) for v in c["values"].values()): c["cell_id"] for c in doc["cells"]}


def _value(cell: dict, key: str):
    return cell["values"][key]


def direction_depends_on_sigma(per_sigma: dict) -> bool:
    pos = any(p["lo95"] is not None and p["lo95"] > 0 for p in per_sigma.values())
    neg = any(p["hi95"] is not None and p["hi95"] < 0 for p in per_sigma.values())
    return pos and neg


def _counts(doc: dict) -> dict:
    runs = doc["runs"]
    return {"runs": len(runs), "ok": sum(r["status"] == "ok" for r in runs),
            "failed": [r["run_id"] for r in runs if r["status"] != "ok"]}


def analyse_exp001(doc: dict, primary: str = "SHRINK_5", base: str = "MEAN") -> dict:
    diffs = paired_differences(doc, primary, base)
    pooled = pooled_stratified(diffs)
    per_sigma = pooled_by_level(doc, diffs, "sigma")
    per_cell = {}
    for c in doc["cells"]:
        iv = summarise_diffs(diffs[c["cell_id"]])
        per_cell[c["cell_id"]] = {"values": c["values"], "n": iv.n, "mean": iv.mean, "sd": iv.sd,
                                  "boot_lo": iv.boot_lo, "boot_hi": iv.boot_hi, "t_lo": iv.t_lo, "t_hi": iv.t_hi,
                                  "std_effect": iv.std_effect}
    h1_supported = pooled["lower_one_sided_95"] is not None and pooled["lower_one_sided_95"] > 0
    # H1b: per sigma, E[D] ordered nu=3 > nu=10 > nu=30; nu=3 vs nu=30 interval overlap.
    sigmas = sorted({_value(c, "sigma") for c in doc["cells"]})
    nus = sorted({_value(c, "nu") for c in doc["cells"]})
    cid = {(_value(c, "nu"), _value(c, "sigma")): c["cell_id"] for c in doc["cells"]}
    h1b_rows, n_ordered, n_overlap = [], 0, 0
    for s in sigmas:
        means = [per_cell[cid[(n, s)]]["mean"] for n in nus]
        ordered = all(means[i] > means[i + 1] for i in range(len(means) - 1))
        a, b = per_cell[cid[(nus[0], s)]], per_cell[cid[(nus[-1], s)]]
        overlap = not (a["boot_lo"] > b["boot_hi"] or b["boot_lo"] > a["boot_hi"])
        n_ordered += ordered
        n_overlap += overlap
        h1b_rows.append({"sigma": s, "means_by_nu": dict(zip([str(n) for n in nus], means)),
                         "ordered_decreasing": ordered, "nu_low_high_intervals_overlap": overlap})
    h1b_contradicted = (n_ordered <= len(sigmas) // 2) or (n_overlap == len(sigmas))
    arrays, weights = [], []
    for s in sigmas:
        arrays += [diffs[cid[(nus[0], s)]], diffs[cid[(nus[-1], s)]]]
        weights += [1 / len(sigmas), -1 / len(sigmas)]
    h1b_est, h1b_boot = _boot_linear(arrays, weights)
    family_p = {"H1b (nu 3 minus nu 30)": p_one_sided_greater(h1b_boot)}
    secondary = {}
    for arm in [a["name"] for a in doc["config"]["arms"]]:
        if arm in (base, primary, "ORACLE"):
            continue
        d = paired_differences(doc, arm, base)
        cells = [d[c["cell_id"]] for c in doc["cells"]]
        est, boots = _boot_linear(cells, [1 / len(cells)] * len(cells))
        key = "H1c (LCB)" if arm == "LCB" else f"{arm} minus {base}"
        family_p[key] = p_one_sided_greater(boots)
        secondary[key] = {**_interval(boots, est), "per_sigma": pooled_by_level(doc, d, "sigma")}
    secondary["H1b (nu 3 minus nu 30)"] = _interval(h1b_boot, h1b_est)
    return {
        "exp_id": doc["exp_id"], "contrast": f"{primary} minus {base}", "metric": "tau_b",
        "counts": _counts(doc), "per_cell": per_cell,
        "H1": {"Dbar": pooled["dbar"], "lo95": pooled["lo95"], "hi95": pooled["hi95"],
               "lower_one_sided_95": pooled["lower_one_sided_95"], "n_cells": pooled["n_cells"],
               "verdict": "supported" if h1_supported else "not supported"},
        "D_sigma": per_sigma,
        "direction_depends_on_sigma": direction_depends_on_sigma(per_sigma),
        "H1b": {"rows": h1b_rows, "n_sigma_ordered": n_ordered, "n_sigma_overlap": n_overlap,
                "verdict": "contradicted" if h1b_contradicted else "supported"},
        "secondary": secondary,
        "holm": holm(family_p),
    }


def _paired_factor_contrast(doc: dict, arm: str, base: str, factor: str, treat, control) -> dict:
    """Same-seed paired difference E[D | factor=treat] - E[D | factor=control] per stratum of the
    other grid factors, and its equal-weight average over strata (stratified bootstrap)."""
    diffs = paired_differences(doc, arm, base)
    seeds = {}
    for r in doc["runs"]:
        seeds.setdefault(r["cell_id"], []).append(r["seed_index"])
    strata: dict[tuple, dict] = {}
    for c in doc["cells"]:
        other = tuple((k, v) for k, v in c["values"].items() if k != factor)
        strata.setdefault(other, {})[c["values"][factor]] = c["cell_id"]
    rows, arrays = [], []
    for other, by in strata.items():
        t_id, c_id = by[treat], by[control]
        t_ok = _ok_seed_values(doc, t_id, arm, base)
        c_ok = _ok_seed_values(doc, c_id, arm, base)
        common = sorted(set(t_ok) & set(c_ok))
        d = np.array([t_ok[s] - c_ok[s] for s in common])
        iv = summarise_diffs(d)
        rows.append({"stratum": dict(other), "n_pairs": iv.n, "mean": iv.mean, "boot_lo": iv.boot_lo,
                     "boot_hi": iv.boot_hi, "excludes_zero": bool(iv.boot_lo > 0 or iv.boot_hi < 0)})
        arrays.append(d)
    est, boots = _boot_linear(arrays, [1 / len(arrays)] * len(arrays))
    return {"factor": factor, "treat": treat, "control": control, "per_stratum": rows,
            **_interval(boots, est), "p_two_sided": p_two_sided(boots),
            "n_strata_excluding_zero": sum(r["excludes_zero"] for r in rows), "_unused": len(diffs)}


def _ok_seed_values(doc: dict, cell_id: str, arm: str, base: str) -> dict[int, float]:
    out = {}
    for r in doc["runs"]:
        if r["cell_id"] != cell_id or r["status"] != "ok":
            continue
        a, b = r["arms"][arm]["tau_b"], r["arms"][base]["tau_b"]
        if a is not None and b is not None:
            out[r["seed_index"]] = a - b
    return out


def analyse_exp002(doc: dict, primary: str = "SHRINK_5", base: str = "MEAN") -> dict:
    res = {"exp_id": doc["exp_id"], "metric": "tau_b", "counts": _counts(doc), "contrasts": {}}
    for arm in (primary, "LCB"):
        lam = _paired_factor_contrast(doc, arm, base, "lam", 2.0, 0.0)
        g_neg = _paired_factor_contrast(doc, arm, base, "gamma", -0.5, 0.0)
        g_pos = _paired_factor_contrast(doc, arm, base, "gamma", 0.5, 0.0)
        for x in (lam, g_neg, g_pos):
            x.pop("_unused")
        block = {"lambda 2 minus 0": lam, "gamma -0.5 minus 0": g_neg, "gamma 0.5 minus 0": g_pos}
        entry = {"contrasts": block}
        if arm == primary:
            entry["holm"] = holm({k: v["p_two_sided"] for k, v in block.items()})
            entry["H1_lambda_verdict"] = ("no detected difference" if lam["n_strata_excluding_zero"] == 0
                                          else "difference detected in at least one stratum")
        else:
            entry["note"] = "reported for LCB as the protocol requires; outside the Holm family"
        res["contrasts"][f"{arm} minus {base}"] = entry
    d = paired_differences(doc, primary, base)
    res["D_per_cell"] = {c["cell_id"]: {"values": c["values"], **_iv(d[c["cell_id"]])} for c in doc["cells"]}
    return res


def _iv(d: np.ndarray) -> dict:
    iv = summarise_diffs(d)
    return {"n": iv.n, "mean": iv.mean, "boot_lo": iv.boot_lo, "boot_hi": iv.boot_hi}


def _sign(x: float) -> int:
    return 0 if x == 0 else (1 if x > 0 else -1)


def analyse_exp003(exp001: dict, exp002: dict, s1_min1: dict, s1_min5: dict, s2: dict, s3: dict, s4: dict,
                   primary: str = "SHRINK_5", base: str = "MEAN") -> dict:
    ref = pooled_stratified(paired_differences(exp001, primary, base))["dbar"]
    ref_sign = _sign(ref)
    out: dict = {"exp_id": "EXP-003", "EXP-001_Dbar": ref,
                 "counts": {k: _counts(v) for k, v in
                            {"S1-min1": s1_min1, "S1-min5": s1_min5, "S2": s2, "S3": s3, "S4": s4}.items()}}

    def pooled(doc, arm=primary, cells=None):
        d = paired_differences(doc, arm, base)
        if cells is not None:
            d = {k: v for k, v in d.items() if k in cells}
        p = pooled_stratified(d)
        sub = {**doc, "cells": [c for c in doc["cells"] if cells is None or c["cell_id"] in cells]}
        return {"Dbar": p["dbar"], "lo95": p["lo95"], "hi95": p["hi95"], "n_cells": p["n_cells"],
                "D_sigma": pooled_by_level(sub, d, "sigma")}

    s1a = pooled(s1_min1)
    s1a["invalidates"] = bool(ref > 0 and s1a["lo95"] <= 0)
    s1b = pooled(s1_min5)
    small = {}
    for r in s1_min5["runs"]:
        ne = (r["diagnostics"] or {}).get("n_evaluated")
        if ne is not None and ne < 20:
            small.setdefault(r["cell_id"], []).append(r["seed_index"])
    s1b["flagged_fewer_than_20_products"] = {k: len(v) for k, v in small.items()}
    s1b["note"] = "the frozen invalidation criterion concerns n >= 1; n >= 5 is reported alongside"
    out["S1"] = {"min1": s1a, "min5": s1b}
    s2r = {}
    for arm in ("SHRINK_5_UP", "SHRINK_5_DOWN"):
        p = pooled(s2, arm)
        p["sign_reversal"] = bool(_sign(p["Dbar"]) != ref_sign)
        s2r[arm] = p
    s2r["SHRINK_5 (check, equals EXP-001)"] = pooled(s2)
    s2r["invalidates"] = any(s2r[a]["sign_reversal"] for a in ("SHRINK_5_UP", "SHRINK_5_DOWN"))
    out["S2"] = s2r
    d_theta = paired_differences(exp002, primary, base)
    d_rep = paired_differences(s3, primary, base)
    rows, n_diff = [], 0
    for c in exp002["cells"]:
        a, b = _iv(d_theta[c["cell_id"]]), _iv(d_rep[c["cell_id"]])
        differs = _sign(a["mean"]) != _sign(b["mean"])
        n_diff += differs
        rows.append({"cell_id": c["cell_id"], "values": c["values"], "theta": a, "theta_rep": b,
                     "sign_differs": differs})
    out["S3"] = {"rows": rows, "n_cells": len(rows), "n_sign_differs": n_diff,
                 "n_sign_differs_lambda2": sum(r["sign_differs"] for r in rows if r["values"]["lam"] == 2.0),
                 "invalidates": n_diff > len(rows) / 2,
                 "pooled_theta_rep": pooled(s3)}
    s4r = {}
    for q in s4["config"]["grid"]["quality"]:
        cells = {c["cell_id"] for c in s4["cells"] if c["values"]["quality"] == q}
        p = pooled(s4, primary, cells)
        p["sign_reversal"] = bool(_sign(p["Dbar"]) != ref_sign)
        s4r[" ".join(str(x) for x in q)] = p
    out["S4"] = {"by_quality": s4r, "invalidates": any(v["sign_reversal"] for v in s4r.values())}
    return out


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating,)):
        o = float(o)
    if isinstance(o, float) and math.isnan(o):
        return None
    return o
