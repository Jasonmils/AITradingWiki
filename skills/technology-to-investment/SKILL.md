---
name: technology-to-investment
description: Map an evidenced technology trend through product feasibility, commercialization, customer adoption, industry structure, bottlenecks, value pools, company exposure, financial materiality, and next-step security research. Use when the user asks which industries or companies may benefit from a technology, where value may accrue, whether an AI trend creates investable opportunities, or how to build an opportunity map. Work wiki-first, preserve stage and evidence boundaries, and ask before saving. Do not use for raw ingestion or a complete current-price decision on one security.
---

# Technology to Investment

Translate technology evidence into an opportunity map without skipping the
commercial and financial bridges.

## Route the request

- Use this skill for industry opportunity maps, value-chain beneficiaries,
  profit-pool analysis, company exposure, and cross-company research priority.
- If mechanism, benchmark, maturity, or forward milestones remain unclear, use
  `$frontier-tech-research` first.
- Route user-supplied raw documents or videos to `$second-brain-ingest`.
- Route a complete one-security dossier, valuation update, or current-price
  decision to `$equity-research`.
- Use `$second-brain-query` for a purely factual Wiki lookup or an existing
  multi-security view that does not require rebuilding the opportunity chain.
- Remain read-only unless the curator approves saving named pages.

## Establish the decision boundary

Resolve:

- technology topic and evidenced `technology_maturity`;
- customer problem, product boundary, buyer, user, and payer;
- geography, policy jurisdiction, value chain, and investment horizon;
- whether the user wants research priority, candidate exposure, or current
  tradability;
- listed securities, listing regimes, currencies, and accounting bases only
  when they are actually required.

Do not guess an ambiguous company, ticker, or commercial relationship.

## Read the evidence chain

1. Read `../second-brain/references/wiki-schema.md`.
2. Read `wiki/index.md` and retrieve relevant Source, Entity, Concept, Event,
   Model, and Synthesis pages.
3. Verify the technology thesis, maturity, competing routes, and invalidation.
4. Identify stale, disputed, vendor-only, rumor-only, or assumption-only links.
5. Re-verify mutable commercialization, company, policy, and market facts from
   primary sources when the answer depends on them.

Keep Wiki facts and current external verification separate, with their own
cutoffs.

## Build the commercialization bridge

Keep these stages distinct:

> Problem validation → demo/POC → paid pilot → formal order → delivery → recognized revenue → profit → FCF

For each stage, record:

- customer and use case;
- product or service boundary;
- evidence, date, evidence type, and confidence;
- price, volume, utilization, deployment, reliability, support, and renewal
  evidence when available;
- next transition and the evidence required to confirm it.

Do not treat a demo, partnership, supply-chain entry, certification, capacity
plan, or TAM estimate as revenue evidence.

## Map industry structure and value capture

Analyze:

- enabling inputs, bottlenecks, complements, substitutes, and integration
  points;
- buyer concentration, supplier concentration, standards, switching costs,
  distribution, regulation, and capital intensity;
- who receives customer value and who has bargaining power;
- whether value accrues to hardware, components, software, services,
  infrastructure, distributors, customers, or competitors;
- how competition, efficiency gains, price decline, or vertical integration may
  redistribute the profit pool.

Separate value creation from value capture. A technically critical component
can still have weak margins or poor shareholder economics.

## Classify company exposure

Use these exposure classes:

- `direct`: evidenced product, customer, deployment, or recognized revenue;
- `indirect`: evidenced enabling input or customer-spend linkage;
- `optionality`: plausible but not yet financially material exposure;
- `spurious`: thematic association without an evidenced economic bridge;
- `disputed`: materially conflicting evidence.

For each company, test:

- ownership, consolidation, and listed-security rights;
- product and value-chain role;
- customer and supplier concentration;
- order, delivery, revenue, margin, capital expenditure, and FCF evidence;
- addressable exposure relative to total company revenue and profit;
- dilution, minority interest, policy, geography, and timing risks.

Do not rank a listed security solely from technical relevance or exposure.

## Prioritize research, not trades

Separate:

1. technology attractiveness;
2. commercialization credibility;
3. industry value-pool attractiveness;
4. company exposure and financial materiality;
5. priority for further security research;
6. valuation and tradability at the current price.

The first five can justify an `$equity-research` handoff. They do not complete
the sixth.

## Answer contract

Return:

1. direct answer, scope, Wiki cutoff, and current verification cutoff;
2. technology maturity and commercialization-stage gate;
3. customer, product, adoption, and unit-economics evidence;
4. value chain, bottlenecks, bargaining power, and likely profit pools;
5. company exposure table using direct, indirect, optionality, spurious, or
   disputed;
6. evidence-classified bridge to company revenue, profit, and FCF;
7. consensus, non-consensus, Codex inference, conflicts, and gaps;
8. catalysts, milestones, monitoring indicators, risks, and invalidation;
9. prioritized follow-up research and the exact evidence still required;
10. securities that justify `$equity-research`, without making an automatic
    current-price call.

## Optional save

When the result is durable:

1. propose exact pages and preview material judgments;
2. wait for explicit curator approval;
3. use `../../templates/commercialization-model.md`,
   `../../templates/industry-opportunity-map.md`, or
   `../../templates/technology-monitoring.md` as applicable;
4. update `wiki/index.md` without removing existing entries;
5. append an operation entry to `wiki/log.md`;
6. preserve superseded or invalidated history.

Do not save an opportunity map or company-priority judgment without approval.
