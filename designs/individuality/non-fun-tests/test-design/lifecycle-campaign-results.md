# PreviewNet lifecycle campaign results (in progress)

Evidence checked on 2026-10-03 UTC. [Campaign run](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758); test commit [`ed563b1`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46). Original attempts and attempt 2 are separate observations.

A is [split and claim](scenarios/payment-burst.md): two calls per actor, in separate waves. B is [recycling](scenarios/synchronised-recycling.md): one coin load per actor, followed by observed ring readiness. No campaign workloads run concurrently.

## Outcomes

Passes below require saved raw extrinsics, canonical block/index matches, successful dispatch events and expected state. State changes alone do not establish a receipt. The saved RPC views are checked for consistency; they are not independent cryptographic consensus proofs.

| Case | Pool entries per People collator | Original attempt | Latest observation | Job |
| --- | --- | --- | --- | --- |
| A100 | Default | Pass: 100 splits + 100 claims | Original pass | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/110910965456) |
| A1,000 | Default | Runner lost during setup | Recovered: 1,000 splits + 1,000 claims | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111088217155) |
| A10,000 | Default | 8,192 split receipts; claims withheld | Same incomplete result | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111091066111) |
| B100 | Default | Runner lost during startup | Download failed before submission; rerun queued | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111094179942) |
| B1,000 | Default | Pass: 1,000 loads and ready members | Passed again | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111094675197) |
| B10,000 | Default | Runner lost during startup | 8,479 original receipts + 245 reconciled; 5,002 observed ready | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111097683539) |
| A8,000 + 2,000 | Default | Pass: 10,000 splits + 10,000 claims | Passed again | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111101176047) |
| A10,000 | 11,000 | Download failed before submission | Recovered: 10,000 splits + 10,000 claims | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111104686208) |
| B8,000 + 2,000 | Default | Pass: 10,000 loads and ready members | Passed again | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111108401107) |
| B10,000 | 11,000 | Pass: 10,000 loads and ready members | Passed again | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111112313624) |
| A20,000 | 22,000 | Runner lost during driver step | 20,000 splits verified; timing gate withheld claims; fixed rerun queued | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111115755886) |
| A40,000 | 44,000 | Runner lost during driver step | 40,000 splits + 40,000 claims verified; CI shutdown timeout | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111118958519) |
| A100,000 | 110,000 | Download failed before submission | Recovered: 100,000 splits + 100,000 claims; CI pass | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111148834636) |
| B20,000 | 22,000 | Pass: 20,000 loads and ready members | Passed again | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111156205276) |
| B40,000 | 44,000 | Runner lost during driver step | Runner lost again; receipt counts unknown | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111161539758) |
| B100,000 | 110,000 | Download failed before submission | Running; no result yet | [Evidence](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111181352051) |

B10,000 attempt 2 has **8,724 verified receipts after reconciliation**, leaving 1,276 without a verified receipt. Reconciliation found 245 additional successful calls in saved finalized blocks. Finality percentiles below retain the original 8,479-watch population; no latency is invented for those 245 calls.

At its last saved readiness observation, B10,000 had 5,002 observed-ready members and 4,998 unobserved. The cutoff was 247.079 s after first submission, at `0x287b5d1475abd3cca4cbc6cb7bf1be2ae36b4ba45ab02111ac595496d854499c`. The receipt audit stopped further observation. Unobserved readiness is not a proven readiness failure.

A20,000 verified all splits, but its 1,005.179 ms launch exceeded the 1,000 ms target. The old timing gate withheld claims. The correction allows claims after valid receipts and state while retaining the timing failure. A40,000 completed both waves and state checks; its process then stayed alive until the 180-minute timeout. Recovery was measured after that timeout, not immediately after the workload.

B40,000 lost runner communication in both attempts. Attempt 2 has no final artifact and its log endpoint returns HTTP 404. Submitted, receipt-verified and readiness counts are unknown. The available evidence does not establish the cause of the runner loss.

## Timings from attempt 2

All values are seconds. Finality is client submission to successful finalized receipt observation, including client/RPC overhead. Its population is successful watched receipts. Readiness is submission to the first finalized poll that finds the member covered by a built ring root; it includes polling delay.

| Case / wave | Finality population | Launch window | Finality p50 | p95 | max |
| --- | --- | --- | --- | --- | --- |
| B1,000 default / recycle | 1,000 | 0.044 | 41.873 | 53.894 | 53.915 |
| B10,000 default / recycle | 8,479 | 0.383 | 133.680 | 217.971 | 229.942 |
| B10,000 enlarged / recycle | 10,000 | 0.394 | 137.158 | 233.401 | 245.434 |
| B10,000 paced / wave-1-recycle | 8,000 | 0.316 | 121.806 | 197.826 | 205.913 |
| B10,000 paced / wave-2-recycle | 2,000 | 0.073 | 46.644 | 66.690 | 70.694 |
| B20,000 enlarged / recycle | 20,000 | 0.799 | 363.694 | 615.855 | 636.100 |
| A1,000 default / claim | 1,000 | 0.051 | 26.155 | 26.173 | 26.186 |
| A1,000 default / split | 1,000 | 0.064 | 29.805 | 29.822 | 29.822 |
| A10,000 default / split | 8,192 | 0.516 | 41.397 | 49.337 | 53.209 |
| A10,000 enlarged / claim | 10,000 | 0.508 | 50.848 | 62.524 | 62.537 |
| A10,000 enlarged / split | 10,000 | 0.532 | 49.233 | 61.232 | 65.056 |
| A10,000 paced / wave-1-claim | 8,000 | 0.370 | 46.637 | 50.734 | 58.501 |
| A10,000 paced / wave-1-split | 8,000 | 0.383 | 49.067 | 53.008 | 60.930 |
| A10,000 paced / wave-2-claim | 2,000 | 0.085 | 44.557 | 44.626 | 44.650 |
| A10,000 paced / wave-2-split | 2,000 | 0.091 | 37.127 | 37.135 | 40.998 |
| A100,000 enlarged / claim | 100,000 | 4.365 | 172.573 | 318.680 | 332.599 |
| A100,000 enlarged / split | 100,000 | 4.956 | 207.971 | 371.987 | 389.557 |
| A20,000 enlarged / split | 20,000 | 1.005 | 62.707 | 98.090 | 98.936 |
| A40,000 enlarged / claim | 40,000 | 1.802 | 84.130 | 131.315 | 132.578 |
| A40,000 enlarged / split | 40,000 | 1.946 | 100.739 | 172.903 | 177.328 |

| Case | Observed-ready population | Readiness p50 | p95 | max | Stage duration |
| --- | --- | --- | --- | --- | --- |
| B10,000 burst default (partial) | 5,002 / 10,000 | 150.951 | 226.736 | 231.871 | Unavailable: no stage summary |
| B1,000 burst default | 1,000 / 1,000 | 80.517 | 105.595 | 105.597 | 110.629 |
| B10,000 burst enlarged | 10,000 / 10,000 | 216.573 | 353.636 | 384.043 | 389.279 |
| B10,000 paced default | 10,000 / 10,000 | 165.930 | 317.952 | 343.236 | 480.183 |
| B20,000 burst enlarged | 20,000 / 20,000 | 524.207 | 809.979 | 845.925 | 851.216 |

Stage duration starts at the first pilot submission and includes its audits, inter-wave claim signing and readiness observation. It excludes network setup, fixture preparation, the one-actor smoke and recovery. A40,000 took 435.545 s and A100,000 took 1,041.877 s through their workload checks; the former subsequently hung during shutdown.

| Payment case (attempt 2) | Stage duration (s) |
| --- | --- |
| A1,000 burst default | 60.029 |
| A10,000 burst enlarged | 160.063 |
| A10,000 paced default | 240.062 |
| A40,000 burst enlarged | 435.545 |
| A100,000 burst enlarged | 1041.877 |

A10,000 default and A20,000 have no completed stage summary: the original audit gate stopped them before claims. Their per-wave measurements are retained above.

## State, backing and recovery

Fixtures seed sufficient-instance coins with backing before measurement. They bypass issuance and wrapped-asset hold setup. These calls consume existing coins; they do not perform an external-asset top-up debit. Split and claim preserve value, and recycling moves coin value into recycler membership. Each available state audit compares the initial and final backing.

Attempt 2 backing stayed at 400,001 units for A100,000 and 40,001 units for B20,000. Both passed the continued-finality and collator recovery checks (64.873 s and 64.820 s respectively). Backing was also unchanged in the incomplete A20,000 and B10,000 workloads; that does not turn them into receipt passes.

## Resource observations

These are sampled peaks. Driver RSS includes fixture preparation and smoke. The runner cgroup includes the network and other processes, rather than one node. Pool maintenance deltas cover the whole driver step. A40,000 includes its long shutdown wait, so that window differs substantially.

| Attempt 2 case | Driver sampled peak RSS (GiB) | Runner cgroup sampled peak (GiB) | Primary pool watched + unwatched peak | Primary pool maintenance sum / count |
| --- | --- | --- | --- | --- |
| A20,000 | 1.304 | 17.358 | 20,000 | 7.287 s / 221 |
| A40,000 | 2.033 | 30.416 | 40,000 | 33.862 s / 3582 |
| A100,000 | 1.992 | 30.870 | 100,000 | 97.714 s / 731 |
| B20,000 | 1.558 | 19.287 | 20,000 | 62.044 s / 424 |

These observations do not measure runtime weight accuracy, block execution wall time or PVF deadline compliance. The watched-plus-unwatched gauge is not the configured ready-pool capacity. Resource observations from successful jobs do not diagnose missing-runner failures.

## Configuration and evidence

PreviewNet engine `7907a3bfa7b2e47535a74b7920086a05ca94773a`; snapshot bundle run `36614342201`, SHA-256 `edab76b213657e499ae9fcb95673a2bf4ca717b78b00caf3d7783fc18b562b4f`. Six relay validators, two People collators and the snapshot's other parachains share one runner. Artificial delay is zero. The A100,000 artifact records 32 visible CPUs with affinity 0–31 and no explicit CPU or memory cap in the runner cgroup; this does not establish unlimited physical memory. Enlarged pools have a 262,144 KiB byte budget on both People collators; default cases apply no pool override.

The [evidence manifest](evidence/lifecycle-2026-10-03/manifest.json) records artifact IDs, hashes, expiry times and verification files. The [observation snapshot](evidence/lifecycle-2026-10-03/observations.json) records counts, timing populations, backing and resource scope. Raw archives, block bodies, signed calls and state responses are retained at `~/Projects/parity/coinage-test-evidence/lifecycle-37029048758`. They are not embedded in this page. The committed summaries and hashes alone cannot reproduce a full receipt audit.

Each successful case artifact contains its fixture, per-wave `*-audit.json`, `*-receipts.json`, `*-state.json`, block evidence, `*-summary.json`, resource samples and `recovery.json`. Recycling also saves `*-readiness.json` and `*-readiness-evidence.jsonl`. The manifest links each artifact; GitHub access and retention limits still apply.

## Pending work

[Targeted rerun](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842) is queued on `ba4bdee5c1a4a7ed725e6a1f34653b7bb39b774c` for B100 and A20,000. It shares the campaign concurrency group and will wait for the active B100,000 job. It includes download retries, preflight preservation, the corrected timing gate and a bounded shutdown diagnostic. These are mitigations; they do not establish why a runner disappeared.

B100,000 still needs final artifact verification. B40,000 remains an attempt with unavailable outcome counts. No production capacity ceiling is claimed.
