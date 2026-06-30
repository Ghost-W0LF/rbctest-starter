# Research Notes

A short reflection on what this prototype demonstrates, its limitations, and where I'd take it as a research direction. The goal here is to think about *oracles* — the long-standing weak point of automated testing — rather than to ship a product.

## What the prototype actually does

The hard part of API/UI testing is rarely *driving* the system; it's deciding whether an observed output is **correct** (the oracle problem). This prototype takes one narrow slice of that:

- It treats an OpenAPI response schema as a **weak, often-stale specification** and uses an LLM to mine candidate oracles from it.
- A second **observation–confirmation** pass discards constraints the model can't re-justify, trading recall for precision — a cheap guard against hallucinated oracles.
- It then separates two failure modes that matter in practice:
  1. **Spec-vs-reality** violations (the spec says non-nullable, the API returns `null`), and
  2. **Downstream-assumption** violations (a field the spec marks nullable that a client treats as always-present — a latent crash).

On the bundled endpoint this surfaced 10 genuine mismatches out of 108 checked constraints. The second category is the interesting one: those are bugs that *neither* a schema validator *nor* the spec author would flag, because they live in the gap between the contract and how the contract is consumed.

## Honest limitations

- **Single endpoint, single response.** No statefulness, no inter-request constraints (e.g. "the `id` returned by POST must appear in the subsequent GET").
- **Oracle precision is unmeasured.** The confirmation pass is a heuristic; I haven't quantified false-positive/negative rates against a labeled set.
- **Schema-bounded.** It mines from the spec, so it can't invent semantic oracles the spec never hints at (value ranges, cross-field invariants like `discount_price <= sell_price`).
- **No grounding in real client code** — the "downstream assumption" set is hand-seeded, not extracted.

## Where I'd take it (and how it connects to your group's work)

These directions are why I'm specifically interested in your lab:

1. **Mining oracles from the consumer, not just the producer.** The downstream-assumption idea becomes powerful if the assumptions are *extracted from real client code* (e.g. how a mobile app deserializes a response) rather than hand-listed. This connects directly to your work on automated oracles for graphically-rich apps (**GLIB**, FSE 2021) — there, the oracle has to be inferred because the spec is essentially absent. I'd like to study oracle inference where the "spec" is the client's expectations.

2. **Bringing this to mobile/UI testing.** My background is production mobile engineering, and your **Guardian** (LLM-based UI exploration, ISSTA 2024) and **TAOPT** (parallel automated mobile UI testing, ASPLOS 2025) tackle the *exploration* side. The complementary open problem is the **oracle** during exploration: when the explorer reaches a new screen, what makes it correct? An LLM oracle conditioned on prior screens + the app's data contracts seems promising and underexplored.

3. **Measuring LLM-oracle reliability.** Oracles that hallucinate are worse than no oracle. Your line on testing and evaluating LLM behavior (e.g. **LLMEffiChecker**) suggests the right rigor: I'd want to characterize *when* LLM-mined oracles are trustworthy, and design confirmation passes with measurable precision rather than the ad-hoc one here.

## Why I built it

I shipped 20+ production mobile apps with real test suites, and repeatedly hit the same wall: the tests that mattered most were the ones asserting *correctness of data and behavior*, and those were the hardest and most manual to write. RBCTest reframed that as an inference problem, so I built a minimal version to understand the mechanics end-to-end. I'd like to work on the parts this prototype only gestures at.
