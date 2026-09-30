# Coinage stress-test findings

Pacing and larger pool settings both produced successful 10,000-top-up runs. The 8,500-transaction first wave exposed dropped-watch outcomes that still require receipt reconciliation. The earlier simultaneous 10,000-top-up run with default pool settings remains the failed baseline; the 1,000-top-up and 1,000-claim passes remain valid.

## Measured results

These results apply to distinct actor keys performing one operation each on a disposable PreviewNet network. They do not measure a sustained real-user population. “Verified receipts” below means successful finalized receipts.

| Scenario / evidence | Result | Verified receipts | Finality p95 | Ring readiness p95 |
| --- | --- | --- | --- | --- |
| [1,000 top-ups][topups-1000] | **PASS** | 1,000 / 1,000 | 53.0 s | 105.6 s |
| [1,000 claims][claims-1000] | **PASS** | 1,000 / 1,000 | 40.9 s | Not applicable |
| [10,000 paced top-ups (7,000 + 3,000)][paced] | **PASS** | 10,000 / 10,000 | 183.0 s | 262.1 s |
| [10,000 simultaneous top-ups, default pool][topups-10000] | **FAIL** | 8,971 / 10,000 | 232.8 s among verified successes | Not reported here |
| [10,000 simultaneous top-ups, enlarged pool][larger-pool] | **PASS** | 10,000 / 10,000 | 256.0 s | 353.1 s |
| [8,500 + 1,500 paced top-ups, default pool][paced-8500] | **FAIL — first-wave receipt gate** | 8,452 / 8,500 submitted; next 1,500 not submitted | Not reported here | Not reported here |

The 1,000-top-up run verified 1,000 actor debits and ready vouchers, with matching held backing. The 1,000-claim run verified that all source coins disappeared and recipient coins had the expected values and ages. **Claim source coins were seeded through privileged fixture setup: this tests claims, not the complete issuance/payment lifecycle.** Network recovery checks passed in these two 1,000-operation runs, the failed default-pool simultaneous burst, the 7,000 + 3,000 paced run and the failed 8,500 first-wave run.

### What limited the simultaneous 10,000-top-up run

All 10,000 submissions were launched; the generator was not the limiting factor. Outcomes were:

- **8,971** verified successful finalized receipts.
- **989** explicit pool-limit rejections.
- **40** additional transactions with dropped watch notifications. State showed their debits and ready vouchers, but their finalized receipts still require reconciliation.

State therefore indicates **9,011 executed top-ups**, while only **8,971 have verified receipts**. State observations do not replace the missing receipts, so the run fails the all-transactions verification requirement.

Node startup logs reported effective ready-pool limits of **8,192 transactions and 20 MiB of transaction bytes**. The 8,971 verified successes are an outcome count across the run, not the pool's capacity. This run exposed admission pressure; it does not show that the chain broke. Network recovery checks passed.

## Paced result: 7,000 + 3,000 — PASS

[Run 36560408065][paced] completed successfully. **All 10,000 top-ups succeeded without manually increasing the transaction-pool limits.** Both People nodes retained ready-pool limits of 8,192 transactions and 20 MiB, confirmed in their startup logs. There were no automatic retries.

The first wave submitted 7,000 transactions in 282 ms. After their successful finalized receipts were verified, the second wave started at 196.0 seconds and submitted 3,000 in 103 ms. Both waves used the same prepared instance. Ring readiness did not gate the second wave.

The final audit verified 10,000 unique successful receipts with no errors. A separate local run of the artifact verifier also matched all 10,000 transaction hashes to the saved block bodies and successful dispatch events. State checks found 10,000 actor debits, 10,000 vouchers included in built roots, and 20,000 asset units held under Coinage.Wrapped, matching the expected backing. The pallet retained its separate minimum free balance of 1. Network recovery and both People-author checks passed.

Finality p95 was 183.0 seconds and ring readiness p95 was 262.1 seconds, each measured from the individual transaction's submission. The measured stage took 410.9 seconds (6 min 51 s), including the wait between waves and final state reads, excluding fixture preparation and the final receipt audit. This demonstrates completion with pacing on this test network; it does not demonstrate admission of 10,000 transactions at once.

## Simultaneous 10,000, enlarged pool — PASS

[Run 36609355696][larger-pool] completed the simultaneous burst. Both People collators used `--pool-limit=11000 --pool-kbytes=40960`; startup logs confirm **11,000 ready transactions / 40 MiB**. All 10,000 submissions launched in 380 ms. There were no retries.

The saved audit reports 10,000 unique verified successful receipts and no audit errors. State checks found 10,000 actor debits, 10,000 ready vouchers and matching held backing. Finality p95 was 256.0 seconds, ring readiness p95 was 353.1 seconds, and the measured stage took 420.7 seconds.

**This configuration completed the simultaneous burst.** Both the transaction-count and byte limits increased, so this run does not isolate which limit mattered. A larger queue does not itself increase block-processing capacity. This is a separate comparison from pacing with unchanged pool limits.

## Paced 8,500 + 1,500 — FAIL at first-wave receipt gate

[Run 36619415692][paced-8500] used the default pool settings and submitted 8,500 transactions in its first wave. It verified **8,452 successful finalized receipts**. Another **48 watches reported “dropped” after first reporting “ready”**; no explicit immediate pool-limit rejections were recorded.

State showed all 8,500 actor debits and matching held backing of 17,000 asset units, including debits for the 48 affected transactions. Their hashes still need reconciliation against finalized blocks and dispatch events. **The 48 are not proven failed transactions, and state changes cannot replace their missing receipts.**

The remaining 1,500 transactions were never submitted because the first-wave receipt gate failed. Network recovery passed. This exposes a gap between watch outcomes and execution evidence; it does not establish an 8,500-transaction capacity limit or a precise failure threshold.

## Experiment in progress: 8,400 + 1,600

[Run 36662212241][paced-8400] was **running** when refreshed on **2026-09-30 at 03:33 UTC (10:33 Asia/Ho_Chi_Minh)**. It had been queued at the earlier check. No result artifacts were available at this refresh.

This experiment uses default pool settings, the same first-wave receipt verification gate and no retries. Inspect its audits and state artifacts before assigning a result; CI status alone does not establish PASS. Refresh again before publication.

## How verification works

Each verified receipt matches a transaction hash to raw extrinsic bytes, its block and index, `System.ExtrinsicSuccess`, and the expected Coinage event. Both local People nodes report the block as canonical and finalized. Separate state checks verify actor debits, held backing and voucher inclusion in built roots for top-ups, or source and recipient coin state for claims. These are trusted local-node observations, not independent cryptographic consensus proofs.

The [evidence guide][guide] explains the reports, receipt audits, raw block evidence, state checks and local artifact verifier. Scenario specifications describe the workload and pass criteria: [top-up burst][topup-spec] and [claim burst][claim-spec].

## Limits of these measurements

- “Actors” means distinct keys performing one operation, not a sustained real-user population.
- The disposable PreviewNet network runs on one CI runner, including two People collators and six relay validators, with no added network delay.
- Submission launch time is not acceptance throughput. Launching the workload within one second does not establish that the nodes accepted it within one second.
- Latency percentiles are measured from each transaction’s submission. Measured stage duration excludes fixture preparation and the final receipt audit.
- Single runs do not establish production capacity, weight accuracy, PVF deadline compliance or a precise failure threshold.
- Claim fixtures bypass issuance. Top-up ring readiness is separate from finality and does not include a wallet's privacy delay.

## Evidence record

Updated-run evidence and statuses checked on **2026-09-30**; the running experiment’s refresh time is recorded above. Earlier findings are retained from the 2026-09-29 review. The commits below identify the test repository revision for each run; they are not runtime or node revisions. Those details belong to each artifact's runtime and provenance files.

| Run (attempt 1) | Test commit | Verification record |
| --- | --- | --- |
| [36534910589][topups-1000] | [`8bffb7d1583e`](https://github.com/paritytech/polkadot-pop-e2e/commit/8bffb7d1583ec6c97c17fe9fd93035c1ba8c40d0) | Top-up receipt audit, state checks and network recovery passed. |
| [36514698770][claims-1000] | [`4e64a30e0273`](https://github.com/paritytech/polkadot-pop-e2e/commit/4e64a30e02732154b4bbf97248e404610809320d) | Claim receipt audit, state checks and network recovery passed; privileged fixture boundary applies. |
| [36537079387][topups-10000] | [`8bffb7d1583e`](https://github.com/paritytech/polkadot-pop-e2e/commit/8bffb7d1583ec6c97c17fe9fd93035c1ba8c40d0) | Partial receipt verification; 40 state-indicated executions still need receipt reconciliation. |
| [36560408065][paced] | [`e2952bc3cea2`](https://github.com/paritytech/polkadot-pop-e2e/commit/e2952bc3cea2cb1b01556663950862e5e9d78b9f) | 10,000 verified receipts; both wave gates, final state checks and network recovery passed. Default pool confirmed in both node logs. |
| [36609355696][larger-pool] | [`e2952bc3cea2`](https://github.com/paritytech/polkadot-pop-e2e/commit/e2952bc3cea2cb1b01556663950862e5e9d78b9f) | Saved audit: 10,000 unique verified receipts, no errors; final state checks passed. Enlarged pool confirmed in startup logs. |
| [36619415692][paced-8500] | [`28ff6d477179`](https://github.com/paritytech/polkadot-pop-e2e/commit/28ff6d47717904567aa2a97b1119b6cd6443f65f) | First-wave gate failed: 8,452 verified receipts, 48 dropped watches requiring reconciliation; all 8,500 debits observed. Recovery passed. |
| [36662212241][paced-8400] | [`28ff6d477179`](https://github.com/paritytech/polkadot-pop-e2e/commit/28ff6d47717904567aa2a97b1119b6cd6443f65f) | Running; no result artifacts at refresh. |

GitHub artifacts expire after **30 days**. Run and commit links identify the evidence but do not preserve it. If durable downloads are needed, archive selected reports, audits, receipts, state checks, raw block evidence and provenance before expiry. This page currently links to the runs; it does not provide a permanent evidence archive.

[topups-1000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36534910589
[claims-1000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36514698770
[topups-10000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36537079387
[paced]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36560408065
[larger-pool]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36609355696
[paced-8500]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36619415692
[paced-8400]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36662212241
[guide]: https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-top-up-burst/ci/previewnet/burst-results.md
[topup-spec]: https://github.com/paritytech/technical-design/blob/indiv-non-fn-testing/designs/individuality/non-fun-tests/test-design/scenarios/top-up-burst.md
[claim-spec]: https://github.com/paritytech/technical-design/blob/indiv-non-fn-testing/designs/individuality/non-fun-tests/test-design/scenarios/claim-burst.md
