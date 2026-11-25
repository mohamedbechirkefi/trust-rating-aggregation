# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Export the published results for the static demo (M5).

Writes ``demo/public/data/results.json`` in the shared template schema
(``lab-demo-results`` 1.0.0) from committed files only: the frozen analysis outputs, the M4
exploratory outputs, the experiment registry, the claims register, the artifact manifest and the
frozen EXP-001 config. Nothing is recomputed from raw runs and nothing is simulated here.

Every ``display`` and ``interval_display`` string is the 4-decimal text the manuscript prints
(``tests/test_demo_export.py`` checks this). The output is deterministic: no timestamps.

Usage: .venv/bin/python scripts/export_demo_data.py [--check]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "demo" / "public" / "data" / "results.json"

ANALYSIS = {e: f"results/confirmatory/analysis/{e}.json" for e in ("EXP-001", "EXP-002", "EXP-003")}
EXPLORATORY = "results/exploratory/m4-sensitivity/m4_exploratory.json"
REGISTRY = "research/experiment_registry.csv"
CLAIMS = "research/claims_register.csv"
MANIFEST = "research/publication/artifact_manifest.json"
CONFIG = "experiments/EXP-001.json"
SOURCES = [*ANALYSIS.values(), EXPLORATORY, REGISTRY, CLAIMS, MANIFEST, CONFIG]

UNIT = "tau-b difference (unitless)"
SIGMAS = ("0.5", "1.0", "1.5")


class ExportError(RuntimeError):
    """Raised when a committed input is missing or inconsistent."""


def f4(x: float, plus: bool = False) -> str:
    s = f"{x:.4f}"
    if s == "-0.0000":
        s = "0.0000"
    return ("+" + s) if plus and x > 0 else s


def est(label: str, mean: float, lo: float | None, hi: float | None, unit: str = UNIT, plus: bool = False) -> dict:
    has = lo is not None and hi is not None
    return {
        "label": label,
        "estimate": mean,
        "ci_low": lo if has else None,
        "ci_high": hi if has else None,
        "ci_level": 0.95 if has else None,
        "unit": unit,
        "display": f4(mean, plus),
        "interval_display": f"{f4(lo)} to {f4(hi)}" if has else None,
    }


def load_json(rel: str) -> dict:
    p = ROOT / rel
    if not p.is_file():
        raise ExportError(f"missing committed input: {rel}")
    return json.loads(p.read_text(encoding="utf-8"))


def sha256(rel: str) -> str:
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def claims_by_experiment() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {"EXP-001": [], "EXP-002": [], "EXP-003": [], "M4-EXPLORATORY": []}
    with (ROOT / CLAIMS).open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            rid, typ = row["result_id"], row["type"]
            for e in ("EXP-001", "EXP-002", "EXP-003"):
                if rid.startswith(e):
                    out[e].append(row["claim_id"])
            if "JRN-0010" in typ:
                out["M4-EXPLORATORY"].append(row["claim_id"])
    return out


def registry() -> dict[str, dict]:
    with (ROOT / REGISTRY).open(encoding="utf-8", newline="") as fh:
        return {r["exp_id"]: r for r in csv.DictReader(fh)}


def exp001(a: dict) -> tuple[dict, list[dict]]:
    h1, ds, sec, holm = a["H1"], a["D_sigma"], a["secondary"], a["holm"]
    if a["counts"]["ok"] != a["counts"]["runs"] or a["counts"]["failed"]:
        raise ExportError("EXP-001 counts are not complete")
    estimates = [est("Dbar: SHRINK_5 minus MEAN, pooled over nine cells (primary)", h1["Dbar"], h1["lo95"], h1["hi95"])]
    estimates.append(est("One-sided 95% lower bound of Dbar (decision quantity for H1)", h1["lower_one_sided_95"], None, None))
    for s in SIGMAS:
        estimates.append(est(f"D_sigma at sigma {s} stars (A-2)", ds[s]["mean"], ds[s]["lo95"], ds[s]["hi95"]))
    for key, lab in (
        ("SHRINK_1 minus MEAN", "SHRINK_1 minus MEAN (secondary, Holm)"),
        ("SHRINK_20 minus MEAN", "SHRINK_20 minus MEAN (secondary, Holm)"),
        ("H1c (LCB)", "H1c: LCB minus MEAN (secondary, Holm)"),
        ("H1b (nu 3 minus nu 30)", "H1b contrast: nu 3 minus nu 30 (secondary, Holm)"),
    ):
        s = sec[key]
        estimates.append(est(lab, s["estimate"], s["lo95"], s["hi95"]))
    lcb = sec["H1c (LCB)"]["per_sigma"]
    verdict = (
        f"H1 {h1['verdict']} (one-sided 95% lower bound {f4(h1['lower_one_sided_95'])} > 0); "
        "the direction depends on the noise level (A-2); "
        f"H1b {a['H1b']['verdict']}; H1c not supported."
    )
    if h1["verdict"] != "supported" or a["H1b"]["verdict"] != "contradicted" or holm["H1c (LCB)"]["reject"]:
        raise ExportError("EXP-001 frozen verdicts differ from the manuscript")
    notes = [
        f"Holm-adjusted p: SHRINK_1 minus MEAN {f4(holm['SHRINK_1 minus MEAN']['p_holm'])}; "
        f"H1c (LCB) {f4(holm['H1c (LCB)']['p_holm'])}. Holm p-values are bootstrap tail probabilities from the same "
        "stratified resamples (D-011, a deviation accepted by the owner with disclosure, D-013).",
        "H1b (the advantage decreases with review count at every noise level) is contradicted: the decreasing order "
        "holds at one of three noise levels.",
        "LCB minus MEAN is negative at every noise level: "
        + ", ".join(f4(lcb[s]["mean"]) for s in SIGMAS)
        + " at sigma 0.5, 1.0 and 1.5.",
        f"{a['counts']['ok']} of {a['counts']['runs']} runs ok, none failed. 20 seeds per cell, N = 200 products, simulated.",
    ]
    rows = []
    for cid in sorted(a["per_cell"]):
        c = a["per_cell"][cid]
        v = c["values"]
        rows.append(dict(est(f"{cid}: nu {v['nu']}, sigma {v['sigma']}", c["mean"], c["boot_lo"], c["boot_hi"]),
                         group=f"sigma {v['sigma']}", kind="cell"))
    for s in SIGMAS:
        rows.append(dict(est(f"D_sigma, sigma {s}", ds[s]["mean"], ds[s]["lo95"], ds[s]["hi95"]),
                         group=f"sigma {s}", kind="summary"))
    rows.append(dict(est("Dbar (pooled, primary)", h1["Dbar"], h1["lo95"], h1["hi95"]), group="pooled", kind="pooled"))
    return {"verdict": verdict, "estimates": estimates, "notes": notes}, rows


def exp002(a: dict) -> tuple[dict, list[dict]]:
    if a["counts"]["ok"] != a["counts"]["runs"] or a["counts"]["failed"]:
        raise ExportError("EXP-002 counts are not complete")
    s5 = a["contrasts"]["SHRINK_5 minus MEAN"]
    lcb = a["contrasts"]["LCB minus MEAN"]
    order = ("lambda 2 minus 0", "gamma -0.5 minus 0", "gamma 0.5 minus 0")
    estimates, rows = [], []
    for arm, block, tested in (("SHRINK_5", s5, True), ("LCB", lcb, False)):
        for k in order:
            c = block["contrasts"][k]
            lab = f"{arm}: change in D, {k}" + ("" if tested else " (outside the Holm family)")
            estimates.append(est(lab, c["estimate"], c["lo95"], c["hi95"]))
            rows.append(dict(est(f"{arm}, {k}", c["estimate"], c["lo95"], c["hi95"]), group=arm, kind="summary"))
    lam = s5["contrasts"]["lambda 2 minus 0"]
    strata = [p for p in lam["per_stratum"] if p["excludes_zero"]]
    verdict = (
        "Selection (lambda): no detected average difference (Holm-adjusted p "
        f"{f4(s5['holm']['lambda 2 minus 0']['p_holm'])}); the frozen contradiction rule is formally not met "
        f"({lam['n_strata_excluding_zero']} of {len(lam['per_stratum'])} stratum intervals exclude 0, in opposite directions). "
        "Exposure (gamma): both contrasts lower D (Holm-adjusted p "
        f"{f4(s5['holm']['gamma -0.5 minus 0']['p_holm'])})."
    )
    notes = [
        "Read as no detected average difference, not as equivalence. The stratum intervals that exclude 0 are "
        + " and ".join(f4(p["mean"]) for p in strata)
        + ".",
        "The protocol's mechanism predicted opposite effects for gamma > 0 and gamma < 0; this was not borne out for "
        "SHRINK_5. LCB followed the predicted pattern.",
        "Holm p-values are bootstrap tail probabilities (D-011, accepted by the owner with disclosure, D-013). "
        f"{a['counts']['ok']} of {a['counts']['runs']} runs ok at sigma 1.0, simulated.",
    ]
    return {"verdict": verdict, "estimates": estimates, "notes": notes}, rows


def exp003(a: dict, ref: dict) -> tuple[dict, list[dict]]:
    for k, c in a["counts"].items():
        if c["ok"] != c["runs"] or c["failed"]:
            raise ExportError(f"EXP-003 {k} counts are not complete")
    conds = [
        ("S1, n >= 1", a["S1"]["min1"], "no"),
        ("S1, n >= 5 (reported)", a["S1"]["min5"], "not applicable"),
        ("S2, centre m + 0.5", a["S2"]["SHRINK_5_UP"], "yes"),
        ("S2, centre m - 0.5", a["S2"]["SHRINK_5_DOWN"], "yes"),
        ("S3, truth theta_rep", a["S3"]["pooled_theta_rep"], "no (vacuous, D-012)"),
        ("S4, Beta(1, 1)", a["S4"]["by_quality"]["beta 1.0 1.0"], "yes"),
        ("S4, Beta(2, 6)/Beta(6, 2) mixture", a["S4"]["by_quality"]["mixture 2.0 6.0 6.0 2.0"], "yes"),
    ]
    if a["S1"]["min1"]["invalidates"] or not a["S2"]["invalidates"] or not a["S4"]["invalidates"] or a["S3"]["invalidates"]:
        raise ExportError("EXP-003 frozen verdicts differ from the manuscript")
    estimates = [est(f"{lab}: pooled D against MEAN (invalidation criterion met: {met})", c["Dbar"], c["lo95"], c["hi95"])
                 for lab, c, met in conds]
    rows = [dict(est("EXP-001 reference", ref["Dbar"], ref["lo95"], ref["hi95"]), group="reference", kind="pooled")]
    rows += [dict(est(lab, c["Dbar"], c["lo95"], c["hi95"]), group=lab.split(",")[0], kind="summary") for lab, c, _ in conds]
    b11 = a["S4"]["by_quality"]["beta 1.0 1.0"]["D_sigma"]["1.5"]
    verdict = (
        "S1 not invalidating; S2 and S4 invalidation criteria met (sign reversal); "
        "S3 criterion not met vacuously: the registered check cannot discriminate by design (D-012)."
    )
    notes = [
        "S3 cannot discriminate: within a cell both truth definitions are strictly increasing in mu, so every rank-only "
        f"metric is identical under the two (sign differs in {a['S3']['n_sign_differs']} of {a['S3']['n_cells']} cells). "
        "This design limitation (D-012) was accepted by the owner with disclosure (D-013); its result carries no evidence.",
        "S1 with n >= 5 has no invalidation criterion; the advantage disappears once products with fewer than five "
        "reviews are removed.",
        f"Under S4 the advantage survives only at sigma 1.5 ({f4(b11['mean'])}, {f4(b11['lo95'])} to {f4(b11['hi95'])}, "
        "for Beta(1, 1)).",
        "EXP-003 conditions are not corrected for multiplicity, as frozen. 1,140 runs, none failed, simulated.",
    ]
    return {"verdict": verdict, "estimates": estimates, "notes": notes}, rows


def exploratory(x: dict) -> dict:
    if x.get("label") != "exploratory":
        raise ExportError("M4 checks are not labelled exploratory")
    p = x["E1"]["precision_at_k"]["per_sigma"]
    lp = x["E1_LCB"]["precision_at_k"]["per_sigma"]["1.5"]
    lr = x["E1_LCB"]["regret_at_k"]
    lr15, lrp = lr["per_sigma"]["1.5"], lr["pooled"]
    e3 = x["E3"]
    estimates = [
        est("E1: SHRINK_5 minus MEAN, precision at 10, sigma 0.5", p["0.5"]["mean"], p["0.5"]["lo95"], p["0.5"]["hi95"], "share of top 10"),
        est("E1: SHRINK_5 minus MEAN, precision at 10, sigma 1.5", p["1.5"]["mean"], p["1.5"]["lo95"], p["1.5"]["hi95"], "share of top 10", plus=True),
        est("E1: LCB minus MEAN, precision at 10, sigma 1.5", lp["mean"], lp["lo95"], lp["hi95"], "share of top 10", plus=True),
        est("E1: regret at 10, MEAN minus LCB, sigma 1.5", lr15["mean"], lr15["lo95"], lr15["hi95"], "stars"),
        est("E1: regret at 10, MEAN minus LCB, pooled", lrp["dbar"], lrp["lo95"], lrp["hi95"], "stars"),
    ]
    for cid, nu in (("c02", 3), ("c05", 10), ("c08", 30)):
        c = e3[cid]
        if c["values"] != {"nu": nu, "sigma": 1.5}:
            raise ExportError(f"E3 {cid} is not the expected cell")
        estimates.append(est(f"E3: D among reviewed products, sigma 1.5, nu {nu}", c["mean"], c["boot_lo"], c["boot_hi"]))
    return {
        "verdict": "No frozen verdict: post hoc checks that change no confirmatory result.",
        "estimates": estimates,
        "notes": [
            "Exploratory and post hoc (JRN-0010). E1 alone contains 30 uncorrected intervals; isolated favourable rows, "
            "such as the LCB's top-of-list gains at sigma 1.5, are hypotheses for a registered follow-up, not findings.",
            "E2 (ties): regenerated catalogues reproduced the committed tau-b values exactly; tie shares depend on review "
            "count and hardly on noise, so ties cannot explain why the sign of D follows noise.",
            "E3 intervals are printed in supplementary Table S6, not in the manuscript body.",
        ],
    }


def sandbox_params(cfg: dict) -> dict:
    """Frozen EXP-001 parameters that the in-browser sandbox uses as its defaults."""
    arms = {a["name"]: a for a in cfg["arms"]}
    q = cfg["base"]["quality"]
    if q[0] != "beta":
        raise ExportError("EXP-001 quality is not a beta family")
    return {
        "source": CONFIG,
        "n_products": cfg["n_products"],
        "quality_beta": [q[1], q[2]],
        "nb_dispersion": cfg["base"]["nb_dispersion"],
        "lcb_z": arms["LCB"]["z"],
        "lcb_prior": arms["LCB"]["prior"],
        "kappa_primary": arms["SHRINK_5"]["kappa"],
        "top_k": cfg["evaluation"]["top_k"],
        "nu_grid": cfg["grid"]["nu"],
        "sigma_grid": cfg["grid"]["sigma"],
    }


def build() -> dict:
    a1, a2, a3 = (load_json(ANALYSIS[e]) for e in ("EXP-001", "EXP-002", "EXP-003"))
    cfg = load_json(CONFIG)
    man = load_json(MANIFEST)
    reg = registry()
    claims = claims_by_experiment()

    e1, fig1 = exp001(a1)
    e2, fig2 = exp002(a2)
    e3, fig3 = exp003(a3, a1["H1"])
    ex = exploratory(load_json(EXPLORATORY))

    def entry(eid: str, body: dict) -> dict:
        r = reg[eid]
        return {
            "id": eid,
            "title": r["title"],
            "status": "complete (confirmatory, frozen protocol v1.0)",
            "verdict": body["verdict"],
            "estimates": body["estimates"],
            "claim_ids": claims[eid],
            "report_path": r["report_location"],
            "notes": body["notes"],
        }

    experiments = [entry("EXP-001", e1), entry("EXP-002", e2), entry("EXP-003", e3)]
    if sorted(reg) != ["EXP-001", "EXP-002", "EXP-003"]:
        raise ExportError("the registry lists experiments this export does not cover")
    experiments.append({
        "id": "M4-EXPLORATORY",
        "title": "Exploratory checks E1 to E3 at M4 (not registered, not confirmatory)",
        "status": "exploratory (post hoc)",
        "verdict": ex["verdict"],
        "estimates": ex["estimates"],
        "claim_ids": claims["M4-EXPLORATORY"],
        "report_path": "results/exploratory/m4-sensitivity/m4_exploratory.md",
        "notes": ex["notes"],
    })

    sp = sandbox_params(cfg)
    assumptions = [
        {"name": "Catalogue size", "value": f"N = {sp['n_products']} products per simulated catalogue", "source": CONFIG},
        {"name": "Latent quality", "value": f"mu = 1 + 4 B stars, B ~ Beta({sp['quality_beta'][0]}, {sp['quality_beta'][1]})",
         "source": "MovieLens 1M fit, rounded to four decimals (manuscript 4.2)"},
        {"name": "Review counts", "value": f"Negative binomial, mean nu times exposure weight, shape {sp['nb_dispersion']}; zero reviews occur",
         "source": "MovieLens 1M fit (manuscript 4.2)"},
        {"name": "Rating model", "value": "r = clip(floor(mu + sigma e + 0.5), 1, 5), e standard normal; sigma is rating noise in stars",
         "source": "manuscript section 3"},
        {"name": "Truth", "value": "theta = expected rating given mu and sigma, computed exactly; known only because the data are simulated",
         "source": "manuscript section 3"},
        {"name": "Design grid", "value": "nu in {3, 10, 30} by sigma in {0.5, 1.0, 1.5} (EXP-001); 20 seeds per cell",
         "source": CONFIG},
        {"name": "Shrinkage", "value": "SHRINK(kappa) = (n xbar + kappa m) / (n + kappa), kappa in {1, 5, 20}, centred at the catalogue mean m",
         "source": "manuscript section 3"},
        {"name": "Lower bound", "value": f"Dirichlet posterior mean minus {sp['lcb_z']} SD, prior of five pseudo-ratings centred on m (A-1)",
         "source": "manuscript section 3"},
        {"name": "Uncertainty", "value": "Two-sided 95% percentile bootstrap over seeds, 10,000 resamples; pooled values stratified by cell",
         "source": "manuscript 4.3"},
    ]
    limitations = [
        "Simulation only. True quality is defined by the model. Nothing here measures real product quality or describes any real platform, and nothing labels any review as fraudulent.",
        "The pooled estimand weights three noise levels equally; its sign depends on that choice. The informative statement is conditional on noise.",
        "The advantage is fragile: a half-star error in the shrinkage centre (S2) or a uniform or bimodal quality population (S4) reverses it.",
        "S3 cannot discriminate between truth definitions for rank metrics (D-012, accepted by the owner with disclosure).",
        "Holm p-values use bootstrap tail probabilities, a choice fixed before data but not in the frozen text (D-011, accepted by the owner with disclosure).",
        "Calibration transfer: dispersion and quality shape come from movie ratings, not product reviews, and the single-noise model misfits held-out star shares.",
        "The noise dependence was seen in exploratory pilots before the freeze; the confirmatory result replicates it and was not predicted blind.",
        "Small effects: the reference gain is 0.0046 tau-b units. Twenty seeds per cell. Herding, manipulation and rater heterogeneity are not modelled.",
    ]
    return {
        "schema": "lab-demo-results",
        "schema_version": "1.0.0",
        "project": "TRUST",
        "question": "When do average ratings misrank products compared with uncertainty-aware estimators?",
        "status_label": "Independent research manuscript / preprint draft, not peer-reviewed. All results are simulated. Protocol v1.0 frozen by the owner on 2026-11-24 before any confirmatory run.",
        "code_revision": man["run_code_revision"],
        "sources": [{"path": s, "sha256": sha256(s)} for s in SOURCES],
        "experiments": experiments,
        "assumptions": assumptions,
        "limitations": limitations,
        "figures": [
            {"id": "FIG-001", "experiment": "EXP-001", "title": "SHRINK_5 minus MEAN in Kendall tau-b, by cell, noise level and pooled",
             "unit": UNIT, "rows": fig1},
            {"id": "FIG-002", "experiment": "EXP-002", "title": "Change in D with reporting selection (lambda) and exposure (gamma)",
             "unit": UNIT, "rows": fig2},
            {"id": "FIG-003", "experiment": "EXP-003", "title": "Pooled D against MEAN under each sensitivity condition",
             "unit": UNIT, "rows": fig3},
        ],
        "sandbox": sp,
    }


def render(data: dict) -> str:
    return json.dumps(data, indent=1, ensure_ascii=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 if the committed file differs")
    args = ap.parse_args(argv)
    text = render(build())
    if args.check:
        same = OUT.is_file() and OUT.read_text(encoding="utf-8") == text
        print("export identical" if same else "export differs")
        return 0 if same else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
