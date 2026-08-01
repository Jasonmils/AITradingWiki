---
name: frontier-tech-research
description: Build or update an evidence-grounded study of one frontier technology topic, including mechanisms, competing routes, benchmark comparability, independent reproduction, technology maturity, bottlenecks, critical unknowns, future milestones, and commercialization implications. Use when the user asks to learn, understand, compare, track, or forecast an AI frontier technology or asks whether a technical trend is real and worth following. Work wiki-first, re-verify mutable technical facts from primary sources, and ask before saving. Do not use for raw-source ingestion, a generic news digest, or a complete one-security investment decision.
---

# Frontier Tech Research

Build a durable technology understanding before translating it into an
industry or security conclusion.

## Route the request

- Use this skill for a technology topic, architecture, model, product class,
  benchmark, scaling path, or future technology trend.
- Route a user-supplied raw document or video to `$second-brain-ingest`.
- Route industry value pools, company beneficiaries, or investment-opportunity
  mapping to `$technology-to-investment` after the technology evidence is
  adequate.
- Route a complete one-security dossier, valuation update, or current-position
  decision to `$equity-research`.
- Remain read-only unless the curator approves saving named pages.

## Establish scope

Resolve:

- the technical question and system boundary;
- relevant versions, releases, tasks, workloads, and time horizon;
- whether the request is explanatory, comparative, or forward-looking;
- competing and substitute routes that must be included;
- the knowledge cutoff and mutable facts requiring current verification.

Do not treat a marketing category as a technically coherent topic until its
mechanism and boundary are defined.

## Read the Vault first

1. Read `../second-brain/references/wiki-schema.md`.
2. Read `wiki/index.md` and search relevant Source, Entity, Concept, Event,
   Model, and Synthesis pages.
3. Follow material `[[wikilinks]]` and identify missing, stale, disputed, or
   vendor-only evidence.
4. Read `raw/` only as a last resort. Never modify it.

State the Wiki cutoff separately from external verification.

## Verify current technical evidence

For mutable or frontier claims, prefer:

1. papers or preprints and their version history;
2. official code repositories, releases, model cards, specifications, and
   standards;
3. authoritative product documentation and official engineering disclosures;
4. independent reproductions and well-specified third-party benchmarks;
5. secondary analysis for discovery and interpretation.

Preserve publication date, retrieval date, version or revision, authorship,
task, dataset, hardware, software, precision, workload, comparison baseline,
and limitations when material.

Apply the existing evidence labels exactly. A paper supports what it reports
under its stated conditions. A vendor roadmap, benchmark, or demo is normally
`company_statement`. Independent reproduction is a separate assertion. A
patent proves neither implementation nor adoption.

## Normalize technical comparisons

Before comparing performance or cost, reconcile or disclose:

- model, checkpoint, task, dataset, and quality target;
- hardware count, memory, topology, numerical precision, sparsity, and power;
- compiler, kernel, framework, runtime, and version;
- input/output length, batch, concurrency, latency, throughput, and
  availability target;
- baseline implementation, measurement window, failures, and exclusions;
- cost boundary, currency, utilization, and amortization.

If the comparison remains materially mismatched, label the result
`disputed` or report it as unavailable. Do not select the favorable figure.

## Determine maturity without promotion

Keep these stages separate:

> Research result → independent reproduction → prototype → pilot → production deployment → scaled adoption

For each claimed transition, cite the evidence and its date. Record the highest
supported `technology_maturity`; do not infer the next stage from press
attention, funding, a benchmark, or a roadmap.

## Build the trend view

Cover:

- problem and why it matters;
- core mechanism and system boundary;
- competing and substitute routes;
- current evidenced maturity;
- performance, cost, reliability, energy, supply-chain, software, regulatory,
  and operational constraints;
- consensus, non-consensus, disputes, and critical unknowns;
- conservative, base, and optimistic development paths;
- dated 6–24 month milestones and longer-horizon dependencies;
- leading indicators, review date, and invalidation conditions;
- commercialization implications without a security recommendation.

Treat trend direction, timing, and probability as `codex_inference` or
`model_assumption` unless directly stated by an attributed source.

## Answer contract

Return:

1. direct answer, scope, Wiki cutoff, and external verification cutoff;
2. current technical state and `technology_maturity`;
3. mechanism and competing-route comparison;
4. benchmark and independent-reproduction audit;
5. evidence-classified findings;
6. bottlenecks, dependencies, disputes, and unknowns;
7. conservative, base, and optimistic paths;
8. dated milestones, monitoring indicators, and invalidation;
9. commercialization implications and evidence gaps;
10. whether `$technology-to-investment` is justified.

Never convert technical appeal into an automatic industry or security call.

## Optional save

When the result is durable:

1. propose exact pages and preview material judgments;
2. wait for explicit curator approval;
3. use `../../templates/concept.md`, `../../templates/technology-model.md`,
   `../../templates/trend-thesis.md`, or
   `../../templates/technology-monitoring.md` as applicable;
4. update `wiki/index.md` without removing existing entries;
5. append an operation entry to `wiki/log.md`;
6. preserve superseded or invalidated history.

Do not save a trend radar, trend thesis, or monitoring page without approval.
