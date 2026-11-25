// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { ResultsError, validateResults } from "./results";

const good = () => JSON.parse(readFileSync("public/data/results.json", "utf8"));

describe("validateResults", () => {
  it("accepts the exported results file", () => {
    expect(validateResults(good()).experiments.length).toBeGreaterThan(0);
  });
  it("rejects a wrong schema name", () => {
    expect(() => validateResults({ ...good(), schema: "other" })).toThrow(ResultsError);
  });
  it("rejects an unsupported major version", () => {
    expect(() => validateResults({ ...good(), schema_version: "2.0.0" })).toThrow(ResultsError);
  });
  it("rejects a missing estimate", () => {
    const r = good();
    delete r.experiments[0].estimates?.[0]?.estimate;
    if (r.experiments[0].estimates.length === 0) r.experiments[0].title = 7;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a non-finite number", () => {
    const r = good();
    r.experiments[0].estimates = [{ label: "x", estimate: "NaN", ci_low: null, ci_high: null, ci_level: null, unit: "" }];
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a half-open interval", () => {
    const r = good();
    r.experiments[0].estimates = [{ label: "x", estimate: 1, ci_low: 0, ci_high: null, ci_level: 0.95, unit: "" }];
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a malformed source hash", () => {
    expect(() => validateResults({ ...good(), sources: [{ path: "a", sha256: "zz" }] })).toThrow(ResultsError);
  });
  it("rejects a results file without the figures extension", () => {
    const r = good();
    delete r.figures;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a figure row without an interval", () => {
    const r = good();
    r.figures[0].rows[0].ci_low = null;
    r.figures[0].rows[0].ci_high = null;
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects a figure row of unknown kind", () => {
    const r = good();
    r.figures[0].rows[0].kind = "decoration";
    expect(() => validateResults(r)).toThrow(ResultsError);
  });
  it("rejects missing or invalid sandbox parameters", () => {
    const a = good();
    delete a.sandbox;
    expect(() => validateResults(a)).toThrow(ResultsError);
    const b = good();
    b.sandbox.n_products = 0;
    expect(() => validateResults(b)).toThrow(ResultsError);
    const c = good();
    c.sandbox.quality_beta = [4.2726];
    expect(() => validateResults(c)).toThrow(ResultsError);
  });
  it("carries every registered experiment and the exploratory checks", () => {
    expect(validateResults(good()).experiments.map((e) => e.id)).toEqual(["EXP-001", "EXP-002", "EXP-003", "M4-EXPLORATORY"]);
  });
});
