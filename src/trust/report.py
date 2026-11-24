# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Report generator: tables, figures and a Markdown report built only from result files.

One generator for every consumer (reports, manuscript, demo, articles; master prompt 11.5).
PDFs go through pandoc to Typst with -V mainfont="Libertinus Serif" (M0 workaround).
"""

from __future__ import annotations

import csv
import json
import math
import os
import subprocess
from html import escape
from pathlib import Path

import numpy as np

from trust.analysis import N_BOOT, paired_differences, pooled_stratified, summarise_diffs
from trust.provenance import sha256_file
from trust.results import import_result, write_json

METRICS = ("tau_b", "spearman", "precision_at_k", "regret_at_k", "coverage", "rmse")
# Defaults: the shared, read-only toolchain one level above the repository (labs/.tools).
_TOOLS = Path(__file__).resolve().parents[3] / ".tools"
PANDOC = os.environ.get("TRUST_PANDOC", str(_TOOLS / "pandoc"))
TYPST_PYTHON = os.environ.get("TRUST_TYPST_PYTHON", str(_TOOLS / "py" / "bin" / "python"))


def fmt(x: float | None, nd: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    return f"{x:.{nd}f}"


def cell_label(cell: dict) -> str:
    vals = cell["values"]
    return ", ".join(f"{k}={v}" for k, v in vals.items()) or "single cell"


def write_metrics_csv(doc: dict, path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = 0
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["exp_id", "label", "run_id", "cell_id", "seed_index", "status", "arm", *METRICS])
        for r in doc["runs"]:
            for arm, m in (r["arms"] or {}).items():
                w.writerow([doc["exp_id"], doc["label"], r["run_id"], r["cell_id"], r["seed_index"], r["status"], arm,
                            *["" if m[k] is None else repr(m[k]) for k in METRICS]])
                rows += 1
            if r["status"] != "ok":
                w.writerow([doc["exp_id"], doc["label"], r["run_id"], r["cell_id"], r["seed_index"], r["status"], "", *[""] * len(METRICS)])
                rows += 1
    return rows


def svg_contrast(title: str, desc: str, labels: list[str], ivs: list, xlabel: str) -> str:
    """Dot-and-interval plot; points are means, bars are 95% percentile bootstrap intervals."""
    w, row_h, left, right, top = 720, 34, 230, 40, 50
    h = top + row_h * len(labels) + 60
    vals = [v for iv in ivs for v in (iv.boot_lo, iv.boot_hi, 0.0) if not math.isnan(v)] or [0.0]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.08 or 0.01
    lo, hi = lo - pad, hi + pad

    def x(v: float) -> float:
        return left + (v - lo) / (hi - lo) * (w - left - right)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">',
        f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>',
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
        f'<text x="{left}" y="24" font-family="sans-serif" font-size="14" fill="#111">{escape(title)}</text>',
        f'<line x1="{x(0):.1f}" y1="{top - 8}" x2="{x(0):.1f}" y2="{top + row_h * len(labels)}" stroke="#888" stroke-dasharray="4 3"/>',
    ]
    for i, (lab, iv) in enumerate(zip(labels, ivs)):
        y = top + row_h * i + row_h / 2
        out.append(f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" font-family="sans-serif" font-size="12" fill="#111">{escape(lab)}</text>')
        if not math.isnan(iv.mean):
            out.append(f'<line x1="{x(iv.boot_lo):.1f}" y1="{y:.1f}" x2="{x(iv.boot_hi):.1f}" y2="{y:.1f}" stroke="#1f4e79" stroke-width="2"/>')
            out.append(f'<circle cx="{x(iv.mean):.1f}" cy="{y:.1f}" r="4.5" fill="#1f4e79"/>')
    yb = top + row_h * len(labels) + 6
    out.append(f'<line x1="{left}" y1="{yb}" x2="{w - right}" y2="{yb}" stroke="#111"/>')
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        out.append(f'<line x1="{x(v):.1f}" y1="{yb}" x2="{x(v):.1f}" y2="{yb + 5}" stroke="#111"/>')
        out.append(f'<text x="{x(v):.1f}" y="{yb + 19}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#111">{v:.3f}</text>')
    out.append(f'<text x="{(left + w - right) / 2:.1f}" y="{yb + 40}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#111">{escape(xlabel)}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def build_report(result_dir: Path, pdf: bool = False) -> dict:
    """Read results.json and run_manifest.json in result_dir; write metrics.csv, summary.json,
    figures/*.svg and report.md (and report.pdf when pdf=True). Returns the summary."""
    result_dir = Path(result_dir)
    res_path = result_dir / "results.json"
    man_path = result_dir / "run_manifest.json"
    doc = import_result(res_path)
    manifest = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else None
    cfg = doc["config"]
    exploratory = doc["label"] == "exploratory"
    arms = [a["name"] for a in cfg["arms"]]
    contrasts = [a for a in arms if a not in ("MEAN", "ORACLE")]
    cells = doc["cells"]
    n_csv = write_metrics_csv(doc, result_dir / "metrics.csv")

    failed = [r["run_id"] for r in doc["runs"] if r["status"] != "ok"]
    degenerate = [(r["run_id"], d) for r in doc["runs"] for d in (r["diagnostics"].get("degenerate") or [])]
    ok_runs = [r for r in doc["runs"] if r["status"] == "ok"]

    summary: dict = {
        "exp_id": doc["exp_id"],
        "label": doc["label"],
        "config_sha256": doc["config_sha256"],
        "results_sha256": sha256_file(res_path),
        "n_runs": len(doc["runs"]),
        "n_failed": len(failed),
        "n_degenerate_flags": len(degenerate),
        "bootstrap_resamples": N_BOOT,
        "contrasts": {},
        "cell_means": {},
        "diagnostics": {},
        "oracle_tau_b_min": None,
    }
    oracle = [r["arms"]["ORACLE"]["tau_b"] for r in ok_runs if "ORACLE" in r["arms"]]
    if oracle:
        summary["oracle_tau_b_min"] = min(v for v in oracle if v is not None)
    for c in cells:
        cid = c["cell_id"]
        rs = [r for r in ok_runs if r["cell_id"] == cid]
        summary["cell_means"][cid] = {
            arm: {m: _mean([r["arms"][arm][m] for r in rs]) for m in METRICS} for arm in arms
        }
        summary["diagnostics"][cid] = {
            k: _mean([r["diagnostics"][k] for r in rs])
            for k in ("share_zero_reviews", "mean_reported", "mean_potential", "s_pool")
        }
    for arm in contrasts:
        diffs = paired_differences(doc, arm, "MEAN")
        per = {cid: summarise_diffs(d) for cid, d in diffs.items()}
        summary["contrasts"][arm] = {
            "per_cell": {cid: iv.__dict__ | {"half_width": iv.half_width} for cid, iv in per.items()},
            "pooled": pooled_stratified(diffs),
        }
    if manifest:
        rt = np.array([t["runtime_s"] for t in manifest["runs"]])
        summary["runtime"] = {
            "per_run_mean_s": float(rt.mean()),
            "per_run_median_s": float(np.median(rt)),
            "per_run_max_s": float(rt.max()),
            "wall_time_s": manifest["wall_time_s"],
            "peak_rss_bytes_process": manifest["peak_rss_bytes_process"],
            "git_revision": manifest["git"]["revision"],
            "git_dirty": manifest["git"]["dirty"],
        }
    write_json(result_dir / "summary.json", _clean(summary))

    # Figure: primary contrast per cell.
    prim, base = cfg["primary_contrast"]
    fig_dir = result_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    figs = []
    if prim in summary["contrasts"]:
        diffs = paired_differences(doc, prim, base)
        ivs = [summarise_diffs(diffs[c["cell_id"]]) for c in cells]
        labs = [f'{c["cell_id"]}: {cell_label(c)}' for c in cells]
        tag = "EXPLORATORY, simulated. " if exploratory else "Simulated. "
        title = f"{doc['exp_id']}: tau-b({prim}) minus tau-b({base}) per cell"
        desc = (f"{tag}Dot-and-interval chart. One row per cell; the dot is the mean paired difference in "
                f"Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval ({N_BOOT} resamples). "
                f"Seeds per cell: {', '.join(str(iv.n) for iv in ivs)}. The dashed line marks zero.")
        name = "fig_primary_contrast.svg"
        (fig_dir / name).write_text(svg_contrast(title, desc, labs, ivs, "difference in Kendall tau-b (unitless)"), encoding="utf-8")
        figs.append((name, title, desc))

    md = render_markdown(doc, summary, figs, manifest, n_csv, failed, degenerate)
    (result_dir / "report.md").write_text(md, encoding="utf-8")
    evidence = {
        "generator": "trust.report.build_report",
        "exp_id": doc["exp_id"],
        "label": doc["label"],
        "config_sha256": doc["config_sha256"],
        "results_path": str(res_path.name),
        "results_sha256": summary["results_sha256"],
        "code_revision": manifest["git"]["revision"] if manifest else None,
        "outputs": {
            "metrics.csv": sha256_file(result_dir / "metrics.csv"),
            "summary.json": sha256_file(result_dir / "summary.json"),
            "report.md": sha256_file(result_dir / "report.md"),
            **{f"figures/{n}": sha256_file(fig_dir / n) for n, _, _ in figs},
        },
    }
    write_json(result_dir / "evidence_manifest.json", evidence)
    if pdf:
        build_pdf(result_dir / "report.md", result_dir / "report.pdf")
    return summary


def _mean(xs: list) -> float | None:
    v = [x for x in xs if x is not None]
    return float(np.mean(v)) if v else None


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, float) and math.isnan(o):
        return None
    return o


def render_markdown(doc, summary, figs, manifest, n_csv, failed, degenerate) -> str:
    cfg = doc["config"]
    exploratory = doc["label"] == "exploratory"
    L = ["<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->", ""]
    L.append(f"# {doc['exp_id']} run report ({doc['label']})")
    L.append("")
    if exploratory:
        L.append("**EXPLORATORY, SIMULATED. Not a finding.** Generated before any protocol freeze. "
                 "These numbers check the pipeline and inform planning; they are not evidence for any hypothesis.")
    else:
        L.append("**Simulated.** Results hold only under the model in `research/protocol.md`.")
    L.append("")
    L.append(f"- Description: {cfg['description']}")
    L.append(f"- Config SHA-256: `{doc['config_sha256']}`")
    L.append(f"- Results SHA-256: `{summary['results_sha256']}` (`results.json`, schema {doc['schema_version']})")
    if manifest:
        g = manifest["git"]
        L.append(f"- Code revision: `{g['revision']}`{' (working tree dirty)' if g['dirty'] else ''}")
        env = manifest["environment"]
        L.append(f"- Environment: Python {env['python']}, numpy {env['packages']['numpy']}, scipy {env['packages']['scipy']}; {env['cpu']}; {env['os']}")
    L.append(f"- Catalogue size N = {cfg['n_products']}; seeds per cell = {cfg['n_seeds']}; cells = {len(doc['cells'])}; runs = {summary['n_runs']}; failed runs = {summary['n_failed']}")
    L.append(f"- Truth: `{cfg['evaluation']['truth']}`; min reviews for evaluation: {cfg['evaluation']['min_reviews']}; top k = {cfg['evaluation']['top_k']}")
    L.append(f"- Machine-readable outputs: `results.json`, `run_manifest.json`, `metrics.csv` ({n_csv} rows), `summary.json`, `evidence_manifest.json`")
    L.append("")
    L.append("## Cells")
    L.append("")
    L.append("| Cell | Grid values | Mean potential raters | Mean reported | Share with zero reviews | s_pool (stars) |")
    L.append("|---|---|---|---|---|---|")
    for c in doc["cells"]:
        d = summary["diagnostics"][c["cell_id"]]
        L.append(f"| {c['cell_id']} | {cell_label(c)} | {fmt(d['mean_potential'], 2)} | {fmt(d['mean_reported'], 2)} | {fmt(d['share_zero_reviews'], 3)} | {fmt(d['s_pool'], 3)} |")
    L.append("")
    L.append("## Mean metric per arm and cell")
    L.append("")
    L.append("Means over seeds. tau-b and Spearman are unitless; precision at k and coverage are proportions; regret at k and RMSE are in stars. Coverage is of nominal 90% intervals among products with at least "
             f"{cfg['evaluation']['coverage_min_n']} reviews.")
    L.append("")
    L.append("| Cell | Arm | tau-b | Spearman | P@k | Regret@k | Coverage | RMSE |")
    L.append("|---|---|---|---|---|---|---|---|")
    for c in doc["cells"]:
        for arm, m in summary["cell_means"][c["cell_id"]].items():
            L.append(f"| {c['cell_id']} | {arm} | {fmt(m['tau_b'])} | {fmt(m['spearman'])} | {fmt(m['precision_at_k'], 3)} | {fmt(m['regret_at_k'])} | {fmt(m['coverage'], 3)} | {fmt(m['rmse'])} |")
    L.append("")
    L.append("## Paired differences in Kendall tau-b against MEAN")
    L.append("")
    L.append(f"Per cell: mean of per-seed paired differences, SD over seeds, 95% percentile bootstrap ({N_BOOT} resamples, fixed seed) and t interval, and the standardised paired difference (mean/SD).")
    L.append("")
    for arm, cdata in summary["contrasts"].items():
        L.append(f"### {arm} minus MEAN")
        L.append("")
        L.append("| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |")
        L.append("|---|---|---|---|---|---|---|---|")
        for cid, iv in cdata["per_cell"].items():
            L.append(f"| {cid} | {iv['n']} | {fmt(iv['mean'])} | {fmt(iv['sd'])} | {fmt(iv['boot_lo'])} to {fmt(iv['boot_hi'])} | {fmt(iv['t_lo'])} to {fmt(iv['t_hi'])} | {fmt(iv['half_width'])} | {fmt(iv['std_effect'], 2)} |")
        L.append("")
    L.append("Pooled over cells (equal weight, stratified bootstrap):")
    L.append("")
    L.append("| Contrast | Cells | Pooled mean | 95% interval | One-sided 95% lower bound |")
    L.append("|---|---|---|---|---|")
    for arm, cdata in summary["contrasts"].items():
        p = cdata["pooled"]
        L.append(f"| {arm} minus MEAN | {p['n_cells']} | {fmt(p['dbar'])} | {fmt(p['lo95'])} to {fmt(p['hi95'])} | {fmt(p['lower_one_sided_95'])} |")
    L.append("")
    for name, title, desc in figs:
        L.append(f'![{title}. {desc}](figures/{name}){{fig-alt="{desc}"}}')
        L.append("")
    L.append("## Checks, failures and degenerate cases")
    L.append("")
    L.append(f"- Minimum ORACLE tau-b over runs: {fmt(summary['oracle_tau_b_min'], 12)} (must equal 1).")
    L.append(f"- Failed runs: {len(failed)}" + (f" ({', '.join(failed)})" if failed else "") + ".")
    L.append(f"- Degenerate-case flags: {len(degenerate)}" + ("" if not degenerate else ": " + "; ".join(f"{r}: {d}" for r, d in degenerate[:20])) + ".")
    if "runtime" in summary:
        rt = summary["runtime"]
        L.append(f"- Runtime per run: mean {rt['per_run_mean_s'] * 1000:.2f} ms, median {rt['per_run_median_s'] * 1000:.2f} ms, max {rt['per_run_max_s'] * 1000:.2f} ms; wall time {rt['wall_time_s']:.2f} s; process peak RSS {rt['peak_rss_bytes_process'] / 2**20:.1f} MiB.")
    L.append("")
    return "\n".join(L)


def build_pdf(md_path: Path, pdf_path: Path) -> None:
    """pandoc (Markdown to Typst, -V mainfont="Libertinus Serif") then the typst Python package."""
    md_path, pdf_path = Path(md_path).resolve(), Path(pdf_path).resolve()
    typ = pdf_path.with_suffix(".typ")
    subprocess.run([PANDOC, str(md_path), "-s", "-t", "typst", "-V", "mainfont=Libertinus Serif",
                    "-V", "papersize=a4", "-o", str(typ)], check=True, cwd=md_path.parent)
    subprocess.run([TYPST_PYTHON, "-c", "import sys, typst; typst.compile(sys.argv[1], output=sys.argv[2])",
                    str(typ), str(pdf_path)], check=True, cwd=md_path.parent)
    typ.unlink()
