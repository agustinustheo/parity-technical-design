# Coinage stress metrics

[Measured-results summary](measured-results.md) · [Lifecycle audit report](lifecycle-campaign-results.md) · [Download extracted data](evidence/stress-metrics-2026-10-05/metrics.json) · [SHA-256 checksum](evidence/stress-metrics-2026-10-05/SHA256SUMS.txt)

## Summary of measured outcomes

These are saved results from four fixed workloads. Pacing and larger pools each completed 10,000 top-ups and claims. Independent saved-evidence checks cover the 150,000-claim run. The lifecycle campaign completed 100,000 split-and-claim actors with 200,000 successful receipts. Recycling completed 40,000 loads and ready members, while the 100,000 case remains incomplete. These finite bursts do not establish sustainable production throughput or a physical capacity ceiling.

The 16 selected lifecycle configurations produced **12 workload passes, one launch-timing failure and three incomplete workloads**. Two workload passes had separate CI shutdown failures. The tables use the selected attempts from the completion audit; earlier setup failures remain in the [original-attempt record](lifecycle-campaign-results.md#outcomes).

## Scope and measurement definitions

A top-up debits an external asset and creates a voucher. A claim transfers one root-seeded source coin into its replacement; it does not add one net live coin. Split-and-claim performs a split and then a claim: **two extrinsics per actor**. Recycling loads an existing coin and observes root coverage. Fixtures and the separate smoke transactions are excluded from workload counts. These tests omit the production wallet planner, chat delivery, TrUAPI and mobile payment experience. Root-seeded claims and lifecycle fixtures bypass issuance and wrapped-asset hold setup; unchanged fixture backing is not proof of normal held-backing accounting.

All displayed timings are **seconds**. Finality is each submission to successful finalized receipt lookup, including client/RPC overhead. Readiness is submission to the first saved finalized observation of ring-root coverage, including polling delay; it is not wallet privacy readiness. Percentiles use the stated population. Later reconciliation adds receipt evidence, never invented latency samples. An em dash means the value is not established in that record; claim ring readiness is not applicable.

Submission windows and calculated launch rates measure the client, not node acceptance or execution throughput. A burst does not execute simultaneously in one block. Lifecycle stage duration includes audits, applicable inter-wave signing and readiness observation, excluding setup, fixtures, smoke and recovery. Top-up and claim stages include waits, observer shutdown and final state reads, excluding fixture preparation, final aggregate receipt audit and recovery. Recovery checks observe liveness and author participation; their durations are not queue-drain measurements.

### Environment and pool configuration

The lifecycle campaign used engine `7907a3bfa7b2e47535a74b7920086a05ca94773a`, snapshot bundle run 36614342201, six relay validators, two People collators and the snapshot’s other parachains on one runner, with zero synthetic delay. Enlarged lifecycle pools used 256 MiB per People collator; default cases applied no override. No individual transactions were retried. Saved scheduling records cover 27 non-overlapping driver executions; they cannot establish orphaned-process lifetimes after lost runners.

The 20,000–100,000 claim series used the same engine and snapshot, `polkadot-weekly2026w33-rc2` binaries, and People runtime `next-people-paseo`, spec 3003000 / transaction version 5. Exact binary and snapshot hashes, runtime limits and configuration are in the download. Its runner reported AMD EPYC 7B13, 16 cores / 32 logical CPUs and about 62.8 GiB RAM; the network and driver shared it. Pool bytes stayed at 40 MiB, while entry limits, fixture batching, query concurrency and launch targets changed. Earlier run-specific configuration and provenance remain linked from the [evidence record](measured-results.md#evidence-record); settings are not assumed identical across series.

## Top-up

[Scenario](scenarios/top-up-burst.md). All rows below retain the original run references and later reconciliation separately. The earlier successful runs are recorded in the existing report; their p95 values are retained at the published precision.

| Run / configuration | Requested / submitted / verified | Finality p50 / p95 / max (N) | Ready; readiness p50 / p95 / max (N) | Stage |
| --- | --- | --- | --- | --- |
| [1,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36534910589/attempts/1) | 1,000 / 1,000 / 1,000 | — / 53.0 / — (1,000) | 1,000; — / 105.6 / — (1,000) | — |
| [7,000 + 3,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36560408065/attempts/1) | 10,000 / 10,000 / 10,000 | — / 183.0 / — (10,000) | 10,000; — / 262.1 / — (10,000) | 410.9 |
| [10,000 burst; 11,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36609355696/attempts/1) | 10,000 / 10,000 / 10,000 | — / 256.0 / — (10,000) | 10,000; — / 353.1 / — (10,000) | 420.7 |
| [10,000 burst; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36537079387/attempts/1) | 10,000 / 10,000 / 9,011 | 136.722 / 232.777 / 244.981 (8,971) | 9,011; 216.392 / 332.522 / 347.910 (9,011) | 628.256 |
| [8,500 + 1,500; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36619415692/attempts/1) | 10,000 / 8,500 / 8,500 | 128.507 / 224.546 / 236.602 (8,452) | 5,869; 155.974 / 231.603 / 236.728 (5,602) | 269.075 |
| [8,400 + 1,600; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36662212241/attempts/1) | 10,000 / 10,000 / 10,000 | 107.019 / 214.931 / 227.177 (10,000) | 10,000; 171.100 / 312.393 / 347.931 (10,000) | 405.548 |

The 7,000 + 3,000 run launched each wave in 0.282 and 0.103 s; the second began about 196 s after the first and waited for verified receipts. The enlarged-pool burst launched in 0.380 s. All three successful rows above verified debits, ready vouchers and matching backing. See the existing [top-up results](measured-results.md#measured-results) for audit and recovery records.

The default simultaneous run has **8,971 original + 40 reconciled = 9,011 receipts**, plus 989 admission rejections. The paced 8,500 case has **8,452 + 48 = 8,500 receipts**; its second wave was withheld. Its original readiness sample covered **5,602**, while later saved state establishes **5,869**. The extra 267 have no new timing samples. The 8,400 + 1,600 case verified all 10,000 receipts and ready members. All three reconciliation cases passed recovery; debited actors and held/wrapped backing were respectively 9,011 / 18,022, 8,500 / 17,000 and 10,000 / 20,000 test-asset units. Reconciliation was verified 30 September 2026 UTC.

[![Top-up and recycling readiness p95, labelled by observed population and configuration](evidence/stress-metrics-2026-10-05/readiness.svg)](evidence/stress-metrics-2026-10-05/readiness.svg)

[![Top-up finality p95 with original sample populations and pool settings](evidence/stress-metrics-2026-10-05/topup-finality.svg)](evidence/stress-metrics-2026-10-05/topup-finality.svg)

## Claim

[Scenario](scenarios/claim-burst.md). Claim ring readiness is not applicable. A pool-ready notification is an RPC observation of transaction-pool state, not voucher readiness.

| Run / pool entries and bytes | Requested / submitted / verified | Client launch | Finality p50 / p95 / max (N) | Stage |
| --- | --- | --- | --- | --- |
| [10,000 burst; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36705343718/attempts/1) | 10,000 / 10,000 / 8,192 | 0.471 | 38.234 / 50.167 / 50.185 (8,192) | — |
| [8,000 + 2,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36719621433/attempts/1) | 10,000 / 10,000 / 10,000 | 0.350 + 0.084 | 38.970 / 50.680 / 50.697 (10,000) | 113.615 |
| [10,000 burst; 11,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36719745986/attempts/1) | 10,000 / 10,000 / 10,000 | 0.433 | 42.903 / 54.686 / 54.694 (10,000) | 88.275 |
| [20,000 burst; 22,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | 20,000 / 20,000 / 20,000 | 0.802 | 65.711 / 93.806 / 93.914 (20,000) | 151.428 |
| [40,000 burst; 44,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | 40,000 / 40,000 / 40,000 | 1.582 | 92.300 / 139.394 / 139.566 (40,000) | 182.521 |
| [100,000 burst; 110,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | 100,000 / 100,000 / 100,000 | 3.930 | 178.521 / 297.346 / 310.339 (100,000) | 410.385 |
| [150,000 burst; 165,000 / 256 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36900802673/attempts/1) | 150,000 / 150,000 / 150,000 | 6.662 | 275.769 / 489.735 / 507.262 (150,000) | 649.976 |

The default 10,000 burst had 989 immediate rejections and 819 dropped watches. Their source coins remained unchanged and recipients absent at the saved state cutoff; dropped watches are not failed-dispatch receipts. The other rows passed receipt and final coin-state checks with unchanged fixture balances, no retries and successful recovery. Claims remove sources and create recipients with the expected instance/value and age 0 → 1. The 150,000 run was independently checked on **2 October 2026 at 03:05 UTC**: 150,000 receipts and saved states, zero mismatches, backing 300,001 → 300,001 raw asset units. The download includes the verifier output and scope; this updates the earlier CI-only verification record.

Fixture balances for the successful 10,000, 20,000, 40,000, 100,000 and 150,000 claim workloads were unchanged at 20,001, 40,001, 80,001, 200,001 and 300,001 raw asset units, respectively.

The paced 10,000 case started its second wave at 52.241 s after the first, following the first 8,000 receipt audit. Its last watch settled at 79.207 s; the enlarged-pool 10,000 burst settled at 55.127 s. For 20,000 / 40,000 / 100,000, preparation took 1,138.347 / 977.091 / 2,440.797 s and launch targets were 1 / 5 / 10 s. The 150,000 launch target was 60 s; its last watch receipt arrived at 509.979 s. Smoke claims are excluded.

The earlier [1,000-claim baseline](measured-results.md#measured-results), [verified memory-fix validation](measured-results.md#verified-1000-claim-validation) and [million-claim generator failure](measured-results.md#claim-generator-memory-retention--2-october-2026) remain separate. The million-claim attempt exhausted the driver’s 24 GiB heap and produced no complete receipt/state audit; it does not establish a chain limit. The [fix](https://github.com/paritytech/polkadot-pop-e2e/commit/932677d50e07052e62d45356a334801dc4630270) bounds retained notifications and cached data without pacing, retries or weaker verification. Its million-notification synthetic regression is not a million-transaction chain run.

### Client notifications and receipt lookup

Re-extracted from saved `claim-burst-transactions.jsonl`, using the submitter’s per-call monotonic start. Each row uses all successful watches in that run. First ready and first inclusion are client notifications; inclusion can precede finality. Finalized notification and completed successful receipt lookup are separate timestamps. Nearest-rank percentiles were recomputed without averaging runs or nodes.

| Run | Observation | N | p50 / p95 / p99 / max (s) |
| --- | --- | --- | --- |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | Submit → first pool-ready | 20,000 | 1.542 / 2.809 / 2.915 / 2.941 |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | Submit → first inclusion | 20,000 | 29.142 / 62.284 / 62.584 / 68.152 |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | Submit → finalized RPC notification | 20,000 | 65.537 / 93.803 / 93.832 / 93.912 |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | Submit → successful receipt lookup | 20,000 | 65.711 / 93.806 / 93.898 / 93.914 |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | Submit → first pool-ready | 40,000 | 3.321 / 6.399 / 6.868 / 7.033 |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | Submit → first inclusion | 40,000 | 73.215 / 112.833 / 112.909 / 112.923 |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | Submit → finalized RPC notification | 40,000 | 92.295 / 139.388 / 139.513 / 139.561 |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | Submit → successful receipt lookup | 40,000 | 92.300 / 139.394 / 139.516 / 139.566 |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | Submit → first pool-ready | 100,000 | 7.435 / 15.268 / 16.088 / 16.441 |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | Submit → first inclusion | 100,000 | 150.106 / 274.796 / 278.924 / 284.309 |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | Submit → finalized RPC notification | 100,000 | 178.341 / 297.157 / 306.360 / 310.250 |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | Submit → successful receipt lookup | 100,000 | 178.521 / 297.346 / 306.367 / 310.339 |

[![Claim finality p50, p95 and p99 by separately labelled pool configuration](evidence/stress-metrics-2026-10-05/claim-finality.svg)](evidence/stress-metrics-2026-10-05/claim-finality.svg)

Client launch rates for the 20,000 / 40,000 / 100,000 bursts were 24,931.9 / 25,284.7 / 25,447.2 submissions/s. These divide submitted count by the unrounded client launch window; they are not sustainable chain TPS.

### Sampled resources and block contents

| Claims / run | Host busy peak | Min available RAM (GiB) | Ready queue peak, primary People node | Driver RSS / heap peak (GiB) | Max canonical proposal (s) |
| --- | --- | --- | --- | --- | --- |
| [20,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | 20.690% | 47.985 | 20,000 | 1.189 / 0.558 | 2.735 |
| [40,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | 25.173% | 46.985 | 37,637 | 1.688 / 0.946 | 2.764 |
| [100,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | 21.290% | 42.980 | 88,185 | 2.820 / 1.567 | 2.970 |

Host and pool values are roughly five-second samples; host CPU is an average across logical CPUs. Driver RSS/heap above uses burst observer samples, with sample timestamps retained in the download. One logical CPU reached about 98% in the 100,000 run. Low host-average CPU does not rule out serial limits. Proposal duration is authoring time, not PVF execution time.

[![Sampled ready-pool occupancy during each separate claim experiment](evidence/stress-metrics-2026-10-05/pool.svg)](evidence/stress-metrics-2026-10-05/pool.svg)

[![Receipt-verified claim counts in canonical finalized blocks](evidence/stress-metrics-2026-10-05/blocks.svg)](evidence/stress-metrics-2026-10-05/blocks.svg)

The 100,000 run used 43 canonical receipt blocks: 42 contained 2,363 claims and the last 754. All 42 full blocks reported `HitBlockWeightLimit`; the last reported `NoMoreTransactions`. Maximum canonical proposal duration was 2.970 s. Enlarging the pool allowed more claims to wait; it did not increase claims per full block. Queue plots use the actual ready gauge, separately for each People collator, during the recorded stage. Watched-plus-unwatched counts are not substituted for this gauge.

## Split-and-claim

[Scenario](scenarios/payment-burst.md). Each actor has one split followed by one claim. Counts below are extrinsics, not actor counts.

| Case / selected attempt | Actors / schedule | Pool entries / bytes | Submitted / verified extrinsics | Workload; CI distinction | Stage (s) |
| --- | --- | --- | --- | --- | --- |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | 100 / burst | 8,192 / 20 MiB (default) | 200 / 200 | workload-pass | 60.021 |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 1,000 / burst | 8,192 / 20 MiB (default) | 2,000 / 2,000 | workload-pass | 60.029 |
| [a10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / burst | 8,192 / 20 MiB (default) | 10,000 / 8,192 | incomplete | — |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / 8,000 + 2,000 paced | 8,192 / 20 MiB (default) | 20,000 / 20,000 | workload-pass | 240.062 |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / burst | 11,000 / 256 MiB | 20,000 / 20,000 | workload-pass | 160.063 |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 20,000 / burst | 22,000 / 256 MiB | 40,000 / 40,000 | launch-timing-failure | 225.207 |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40,000 / burst | 44,000 / 256 MiB | 80,000 / 80,000 | workload-pass; shutdown failed | 435.545 |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 100,000 / burst | 110,000 / 256 MiB | 200,000 / 200,000 | workload-pass | 1,041.877 |

| Case | Wave | Submitted | Launch (s) | Client launches/s | Finality N | p50 / p95 / max (s) |
| --- | --- | --- | --- | --- | --- | --- |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | split-split | 100 | 0.006 | 18,093.620 | 100 | 27.687 / 27.688 / 27.688 |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | split-claim | 100 | 0.004 | 26,702.063 | 100 | 31.710 / 31.712 / 31.714 |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 1,000 | 0.064 | 15,674.771 | 1,000 | 29.805 / 29.822 / 29.822 |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-claim | 1,000 | 0.051 | 19,451.906 | 1,000 | 26.155 / 26.173 / 26.186 |
| [a10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 10,000 | 0.516 | 19,380.553 | 8,192 | 41.397 / 49.337 / 53.209 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-wave-1-split | 8,000 | 0.383 | 20,863.676 | 8,000 | 49.067 / 53.008 / 60.930 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-wave-1-claim | 8,000 | 0.370 | 21,615.986 | 8,000 | 46.637 / 50.734 / 58.501 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-wave-2-split | 2,000 | 0.091 | 22,058.290 | 2,000 | 37.127 / 37.135 / 40.998 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-wave-2-claim | 2,000 | 0.085 | 23,554.426 | 2,000 | 44.557 / 44.626 / 44.650 |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 10,000 | 0.532 | 18,811.278 | 10,000 | 49.233 / 61.232 / 65.056 |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-claim | 10,000 | 0.508 | 19,687.561 | 10,000 | 50.848 / 62.524 / 62.537 |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | split-split | 20,000 | 1.100 | 18,187.728 | 20,000 | 57.641 / 81.841 / 86.024 |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | split-claim | 20,000 | 0.949 | 21,074.328 | 20,000 | 49.999 / 73.645 / 73.964 |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 40,000 | 1.946 | 20,557.721 | 40,000 | 100.739 / 172.903 / 177.328 |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-claim | 40,000 | 1.802 | 22,196.872 | 40,000 | 84.130 / 131.315 / 132.578 |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 100,000 | 4.956 | 20,179.017 | 100,000 | 207.971 / 371.987 / 389.557 |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-claim | 100,000 | 4.365 | 22,909.419 | 100,000 | 172.573 / 318.680 / 332.599 |

At 20,000 actors, the corrected rerun verified all 40,000 receipts and states, but split launch took **1.099643 s against a 1.000 s target**. It remains a generator launch-timing failure. At 40,000, all 80,000 receipts passed but CI shutdown timed out. At 100,000, all 200,000 receipts and the workload passed. Default 10,000 withheld claims after the incomplete split wave.

## Recycling

[Scenario](scenarios/synchronised-recycling.md). Each actor submits one coin-load extrinsic; root coverage is a separate observation.

| Case / selected attempt | Actors / schedule | Pool entries / bytes | Submitted / verified extrinsics | Workload; CI distinction | Stage (s) |
| --- | --- | --- | --- | --- | --- |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 100 / burst | 8,192 / 20 MiB (default) | 100 / 100 | workload-pass | 55.343 |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 1,000 / burst | 8,192 / 20 MiB (default) | 1,000 / 1,000 | workload-pass | 110.629 |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / burst | 8,192 / 20 MiB (default) | 10,000 / 8,724 | incomplete | — |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / 8,000 + 2,000 paced | 8,192 / 20 MiB (default) | 10,000 / 10,000 | workload-pass | 480.183 |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / burst | 11,000 / 256 MiB | 10,000 / 10,000 | workload-pass | 389.279 |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20,000 / burst | 22,000 / 256 MiB | 20,000 / 20,000 | workload-pass | 851.216 |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | 40,000 / burst | 44,000 / 256 MiB | 40,000 / 40,000 | workload-pass; shutdown failed | 1,563.826 |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 100,000 / burst | 110,000 / 256 MiB | 100,000 / 60,990 | incomplete | — |

| Case | Wave | Submitted | Launch (s) | Client launches/s | Finality N | p50 / p95 / max (s) |
| --- | --- | --- | --- | --- | --- | --- |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | recycle-recycle | 100 | 0.006 | 17,828.808 | 100 | 35.676 / 35.677 / 35.677 |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 1,000 | 0.044 | 22,618.230 | 1,000 | 41.873 / 53.894 / 53.915 |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 10,000 | 0.383 | 26,115.716 | 8,479 | 133.680 / 217.971 / 229.942 |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-wave-1-recycle | 8,000 | 0.316 | 25,330.817 | 8,000 | 121.806 / 197.826 / 205.913 |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-wave-2-recycle | 2,000 | 0.073 | 27,349.204 | 2,000 | 46.644 / 66.690 / 70.694 |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 10,000 | 0.394 | 25,383.404 | 10,000 | 137.158 / 233.401 / 245.434 |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 20,000 | 0.799 | 25,021.593 | 20,000 | 363.694 / 615.855 / 636.100 |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | recycle-recycle | 40,000 | 1.428 | 28,002.665 | 40,000 | 606.384 / 1,095.313 / 1,143.690 |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 100,000 | 3.692 | 27,083.397 | 60,982 | 925.565 / 1,709.561 / 1,794.058 |

| Case | Observed ready | Timing N | Readiness p50 / p95 / max (s) | Observation cutoff (s) |
| --- | --- | --- | --- | --- |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 100 | 100 | 50.339 / 50.341 / 50.341 | 50.341 |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 1,000 | 1,000 | 80.517 / 105.595 / 105.597 | 105.627 |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 5,002 | 5,002 | 150.951 / 226.736 / 231.871 | 247.079 |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 | 10,000 | 165.930 / 317.952 / 343.236 | 475.169 |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 | 10,000 | 216.573 / 353.636 / 384.043 | 384.264 |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20,000 | 20,000 | 524.207 / 809.979 / 845.925 | 846.185 |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | 40,000 | 40,000 | 910.867 / 1,485.140 / 1,558.509 | 1,558.766 |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 39,917 | 39,917 | 992.583 / 1,718.515 / 1,797.529 | 1,797.949 |

Default 10,000: **8,479 + 245 reconciled = 8,724 receipts**; 1,276 without receipts. Readiness observed 5,002 of 10,000 by 247.079 s. At 40,000, receipts, state and readiness all passed, but CI hit its two-minute shutdown guard with a retained TCP socket; its owner is not established. Recovery passed in 64.917 s after the guard. At 100,000, all calls were submitted: **60,982 + 8 = 60,990 receipts**, with 39,010 without verified receipts; 39,917 ready and 60,083 unobserved at 1,797.949 s. State has 61,851 members, including 861 state-only outcomes. Blocks 173363, 173365 and 173366 are absent from saved raw evidence. Stage duration is unavailable. Missing receipts and unobserved readiness do not prove non-execution or failure.

### Lifecycle state, backing and sampled resources

State and backing observations below are per selected case. Balances are raw fixture asset units. These lifecycle operations do not perform external-asset top-up debits. Resource windows cover the entire driver step, potentially including fixtures and smoke. Network service cgroup memory includes multiple processes, not one collator. Pool maintenance counters in the data cover their stated epoch window and are not runtime execution timings.

| Case | Backing before → after | Wave state checks | Recovery | Driver RSS GiB | Network cgroup GiB | Resource samples |
| --- | --- | --- | --- | --- | --- | --- |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | 401 → 401 | Pass (2 waves) | Pass | 0.304 | 14.308 | 73 |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 4001 → 4001 | Pass (2 waves) | Pass | 0.408 | 14.384 | 74 |
| [a10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40001 → 40001 | Incomplete | Pass | 0.803 | 15.432 | 88 |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 201 → 201 | Pass | True | 0.239 | 15.463 | 82 |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 2001 → 2001 | Pass | True | 0.381 | 14.663 | 93 |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20001 → 20001 | Incomplete | Pass | 1.002 | 16.293 | 133 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40001 → 40001 | Pass (4 waves) | Pass | 0.844 | 16.199 | 135 |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40001 → 40001 | Pass (2 waves) | Pass | 0.901 | 16.046 | 119 |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20001 → 20001 | Pass (2 waves) | Pass | 0.887 | 16.631 | 178 |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20001 → 20001 | Pass | True | 0.854 | 16.307 | 150 |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 80001 → 80001 | Pass (2 waves) | Pass | 1.290 | 19.588 | 154 |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 160001 → 160001 | Pass (2 waves) | Pass | 2.033 | 30.416 | 2,160 |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 400001 → 400001 | Pass (2 waves) | Pass | 1.992 | 30.870 | 451 |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40001 → 40001 | Pass | True | 1.558 | 19.287 | 275 |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | 80001 → 80001 | Pass | True | 2.431 | 25.027 | 484 |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 200001 → 200001 | Incomplete | Pass | 4.390 | 31.964 | 673 |

[![Lifecycle finality percentiles with original timing populations](evidence/stress-metrics-2026-10-05/lifecycle-finality.svg)](evidence/stress-metrics-2026-10-05/lifecycle-finality.svg)

[![Selected requested, submitted and verified counts, and sampled claim driver memory](evidence/stress-metrics-2026-10-05/outcomes-resources.svg)](evidence/stress-metrics-2026-10-05/outcomes-resources.svg)

## Evidence-backed interpretation

Pool configuration changes backlog capacity, while block weight limits still govern what fits into a block. Pacing and a larger queue both completed particular workloads; comparisons also involve different actors, pool bytes, launch targets and harness versions. The highest passing run is not a measured physical limit. These observations do not establish production capacity, runtime-weight accuracy, block execution wall time or PVF deadline compliance.

Successful receipts require raw extrinsic hash, canonical block/index, `System.ExtrinsicSuccess` and expected operation evidence. State checks are separate. Saved finalized views from local RPC nodes establish evidence consistency, not independent cryptographic consensus or storage proofs. This report re-extracts measurements; it does not rerun workloads or claim a new full receipt audit. Original verification dates are retained below.

## References and extracted data

[Machine-readable metrics](evidence/stress-metrics-2026-10-05/metrics.json) and [checksum](evidence/stress-metrics-2026-10-05/SHA256SUMS.txt) contain selected measurements, source filenames/hashes, run attempts, runtime/binary provenance and sampled time series. Numeric duration fields use seconds. Millisecond source fields were converted and renamed with a `Seconds` suffix; original source hashes still identify the unmodified preserved files. These small hosted files are not full raw receipt archives. GitHub artifacts expire after 30 days; locally preserved raw archives survive expiry but are not public downloads.

Lifecycle cases were audited **3 October 2026 UTC**. Exact artifact IDs, archive digests and expiry dates are in the [manifest](evidence/lifecycle-2026-10-03/manifest.json); original-attempt history and per-job links are in the [pinned audited report](https://github.com/paritytech/technical-design/blob/e26a47902fa1cbc1a9dd5dca80d1dc5a2657a508/designs/individuality/non-fun-tests/test-design/lifecycle-campaign-results.md).

| Case / attempt | Test commit | Verification file |
| --- | --- | --- |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a100-verification.json](evidence/lifecycle-2026-10-03/a100-verification.json) |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a1000-attempt-2-verification.json](evidence/lifecycle-2026-10-03/a1000-attempt-2-verification.json) |
| [a10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [coinage-split-10000-burst-default-pilot-37029048758-2-split-pilot-split-subset-verification.json](evidence/lifecycle-2026-10-03/coinage-split-10000-burst-default-pilot-37029048758-2-split-pilot-split-subset-verification.json) |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | [`ba4bdee5c1a4`](https://github.com/paritytech/polkadot-pop-e2e/commit/ba4bdee5c1a4a7ed725e6a1f34653b7bb39b774c) | [b100-targeted-verification.txt](evidence/lifecycle-2026-10-03/b100-targeted-verification.txt) |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b1000-attempt-2-verification.json](evidence/lifecycle-2026-10-03/b1000-attempt-2-verification.json) |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [coinage-recycle-10000-burst-default-pilot-37029048758-2-recycle-pilot-recycle-subset-verification.json](evidence/lifecycle-2026-10-03/coinage-recycle-10000-burst-default-pilot-37029048758-2-recycle-pilot-recycle-subset-verification.json) |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a-paced-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/a-paced-attempt-2-verification.txt) |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a-pool-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/a-pool-attempt-2-verification.txt) |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b-paced-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/b-paced-attempt-2-verification.txt) |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b-pool-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/b-pool-attempt-2-verification.txt) |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | [`ba4bdee5c1a4`](https://github.com/paritytech/polkadot-pop-e2e/commit/ba4bdee5c1a4a7ed725e6a1f34653b7bb39b774c) | [a20000-targeted-workload-verification.json](evidence/lifecycle-2026-10-03/a20000-targeted-workload-verification.json) |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a40000-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/a40000-attempt-2-verification.txt) |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a100000-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/a100000-attempt-2-verification.txt) |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b20000-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/b20000-attempt-2-verification.txt) |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | [`ba4bdee5c1a4`](https://github.com/paritytech/polkadot-pop-e2e/commit/ba4bdee5c1a4a7ed725e6a1f34653b7bb39b774c) | [b40000-targeted-verification.txt](evidence/lifecycle-2026-10-03/b40000-targeted-verification.txt) |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b100000-receipts-reconciliation.json](evidence/lifecycle-2026-10-03/b100000-receipts-reconciliation.json) |

| Claim run (attempt 1) | Test commit | Verification date / source |
| --- | --- | --- |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | [`23a884c644db`](https://github.com/paritytech/polkadot-pop-e2e/commit/23a884c644dba50805f7b9373ad45d2529bb888f) | 2026-10-01T08:24:18.422021+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | [`39d2961bb794`](https://github.com/paritytech/polkadot-pop-e2e/commit/39d2961bb7940ee0dd07b970968bc4be034a9608) | 2026-10-01T08:57:55.492162+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | [`b7451cd74bbe`](https://github.com/paritytech/polkadot-pop-e2e/commit/b7451cd74bbe71799ab9bc8e01a69696ab043217) | 2026-10-01T10:05:49.982071+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36900802673](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36900802673/attempts/1) | [`932677d50e07`](https://github.com/paritytech/polkadot-pop-e2e/commit/932677d50e07052e62d45356a334801dc4630270) | 2026-10-02T03:05:11.110954+00:00; `claim-burst-summary.json`, `local-verification.json` |

Earlier top-up and 10,000-claim commits, original verification dates and artifact IDs remain in the [existing evidence record](measured-results.md#evidence-record). The [claim methodology](https://github.com/paritytech/polkadot-pop-e2e/blob/dfdc44a75bc91ea1610742b42b4e5278f4ad42fd/ci/previewnet/burst-results.md) is separate from the [top-up evidence guide](https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-top-up-burst/ci/previewnet/burst-results.md).
