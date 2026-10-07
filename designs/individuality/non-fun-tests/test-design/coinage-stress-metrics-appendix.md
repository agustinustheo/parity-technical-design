# Appendix: Coinage measured results

The tables below preserve the detailed measurements and evidence references behind the [Coinage stress metrics report](coinage-stress-metrics.md). If you'd rather work with the numbers directly, you can [download the extracted data](evidence/stress-metrics-2026-10-05/metrics.json). All timings are seconds; N is the timing sample count. An em dash means the record does not establish that measurement. See the report’s [measurement definitions](coinage-stress-metrics.md#measurement-definitions) and [environment](coinage-stress-metrics.md#environment-and-pool-configuration) before comparing configurations.

Finality ends at successful finalized receipt lookup. Readiness ends at the first saved finalized observation of root coverage. Reconciled counts do not create new timing samples. Stage duration excludes fixtures, smoke and recovery; workflow-specific boundaries remain in the report.

## Top-up measurements

Timing populations remain original after reconciliation. The ready count can include later state observations; its timing population is shown separately.

| Run / configuration | Requested / submitted / verified | Finality p50 / p95 / max (N) | Ready; readiness p50 / p95 / max (N) | Stage |
| --- | --- | --- | --- | --- |
| [1,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36534910589/attempts/1) | 1,000 / 1,000 / 1,000 | — / 53.0 / — (1,000) | 1,000; — / 105.6 / — (1,000) | — |
| [7,000 + 3,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36560408065/attempts/1) | 10,000 / 10,000 / 10,000 | — / 183.0 / — (10,000) | 10,000; — / 262.1 / — (10,000) | 410.9 |
| [10,000 burst; 11,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36609355696/attempts/1) | 10,000 / 10,000 / 10,000 | — / 256.0 / — (10,000) | 10,000; — / 353.1 / — (10,000) | 420.7 |
| [10,000 burst; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36537079387/attempts/1) | 10,000 / 10,000 / 9,011 | 136.722 / 232.777 / 244.981 (8,971) | 9,011; 216.392 / 332.522 / 347.910 (9,011) | 628.256 |
| [8,500 + 1,500; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36619415692/attempts/1) | 10,000 / 8,500 / 8,500 | 128.507 / 224.546 / 236.602 (8,452) | 5,869; 155.974 / 231.603 / 236.728 (5,602) | 269.075 |
| [8,400 + 1,600; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36662212241/attempts/1) | 10,000 / 10,000 / 10,000 | 107.019 / 214.931 / 227.177 (10,000) | 10,000; 171.100 / 312.393 / 347.931 (10,000) | 405.548 |

## Claim measurements

Claims do not require ring readiness. Launch windows measure the client.

| Run / pool entries and bytes | Requested / submitted / verified | Client launch | Finality p50 / p95 / max (N) | Stage |
| --- | --- | --- | --- | --- |
| [10,000 burst; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36705343718/attempts/1) | 10,000 / 10,000 / 8,192 | 0.471 | 38.234 / 50.167 / 50.185 (8,192) | — |
| [8,000 + 2,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36719621433/attempts/1) | 10,000 / 10,000 / 10,000 | 0.350 + 0.084 | 38.970 / 50.680 / 50.697 (10,000) | 113.615 |
| [10,000 burst; 11,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36719745986/attempts/1) | 10,000 / 10,000 / 10,000 | 0.433 | 42.903 / 54.686 / 54.694 (10,000) | 88.275 |
| [20,000 burst; 22,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | 20,000 / 20,000 / 20,000 | 0.802 | 65.711 / 93.806 / 93.914 (20,000) | 151.428 |
| [40,000 burst; 44,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | 40,000 / 40,000 / 40,000 | 1.582 | 92.300 / 139.394 / 139.566 (40,000) | 182.521 |
| [100,000 burst; 110,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | 100,000 / 100,000 / 100,000 | 3.930 | 178.521 / 297.346 / 310.339 (100,000) | 410.385 |
| [150,000 burst; 165,000 / 256 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36900802673/attempts/1) | 150,000 / 150,000 / 150,000 | 6.662 | 275.769 / 489.735 / 507.262 (150,000) | 649.976 |

## Client notifications and receipt lookup

All timings are seconds, from each submission. Finalized RPC notification and successful receipt lookup are separate observations.

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

## Claim resources

Host and pool metrics are approximately five-second samples. Driver memory uses burst observer samples. Proposal duration is authoring time, not PVF execution.

| Claims / run | Host busy peak | Min available RAM (GiB) | Ready queue peak, primary People node | Driver RSS / heap peak (GiB) | Max canonical proposal (s) |
| --- | --- | --- | --- | --- | --- |
| [20,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | 20.690% | 47.985 | 20,000 | 1.189 / 0.558 | 2.735 |
| [40,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | 25.173% | 46.985 | 37,637 | 1.688 / 0.946 | 2.764 |
| [100,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | 21.290% | 42.980 | 88,185 | 2.820 / 1.567 | 2.970 |

## Split-and-claim outcomes

Two extrinsics per actor. Workload outcome and CI shutdown outcome remain separate.

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

## Split-and-claim wave timings

Client launches/s is submitted count divided by the unrounded submission window; it is not chain throughput.

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

## Recycling outcomes

One coin-load extrinsic per actor, followed by a separate root-coverage observation.

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

## Recycling wave timings

Percentiles use original successful watches; reconciled receipts add no timing samples.

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

## Recycling readiness

Readiness includes finalized polling delay and is not wallet privacy readiness. Unobserved readiness is not a proven failure.

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

## Lifecycle state and resources

Backing uses raw fixture asset units. Resource samples cover the driver step, potentially including fixtures and smoke; network cgroup memory includes multiple processes.

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

## Lifecycle evidence references

Selected attempts were audited on 3 October 2026 UTC.

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

## Claim evidence references

Original independent verification dates are retained below.

| Claim run (attempt 1) | Test commit | Verification date / source |
| --- | --- | --- |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | [`23a884c644db`](https://github.com/paritytech/polkadot-pop-e2e/commit/23a884c644dba50805f7b9373ad45d2529bb888f) | 2026-10-01T08:24:18.422021+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | [`39d2961bb794`](https://github.com/paritytech/polkadot-pop-e2e/commit/39d2961bb7940ee0dd07b970968bc4be034a9608) | 2026-10-01T08:57:55.492162+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | [`b7451cd74bbe`](https://github.com/paritytech/polkadot-pop-e2e/commit/b7451cd74bbe71799ab9bc8e01a69696ab043217) | 2026-10-01T10:05:49.982071+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36900802673](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36900802673/attempts/1) | [`932677d50e07`](https://github.com/paritytech/polkadot-pop-e2e/commit/932677d50e07052e62d45356a334801dc4630270) | 2026-10-02T03:05:11.110954+00:00; `claim-burst-summary.json`, `local-verification.json` |

## Merchant fan-in measurements

Run [37510457575, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1), test commit [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5). Each transfer is one claim into a fresh destination key of one merchant, from a fixture-prepared coin. Attempt 2 was queued automatically and cancelled before any job ran; it has no results. Launch windows measure the client, not chain throughput.

| Transfers | Pattern | Pool entries / bytes | Watch-finalized | Receipt-verified | State-verified | Client launch | Finality p50 / p95 / max (N) | Result | Job |
| ---: | --- | --- | ---: | --- | ---: | --- | --- | --- | --- |
| 100 | Burst | 8,192 / 20 MiB (default) | 100 | 100 | 100 | 0.006 | 35.72 / 35.72 / 35.73 (100) | Passed | [112480491326](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112480491326) |
| 1,000 | Burst | 8,192 / 20 MiB (default) | 1,000 | 1,000 | 1,000 | 0.080 | 30.42 / 30.45 / 30.45 (1,000) | Passed | [112487225834](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112487225834) |
| 10,000 | Burst | 8,192 / 20 MiB (default) | 8,193 | 8,193 original + 818 reconciled = 9,011 | 9,011 | 0.543 | 41.25 / 45.31 / 45.35 (8,193) | **Failed** completion target | [112493393120](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112493393120) |
| 10,000 | Waves 8,000 + 2,000 | 8,192 / 20 MiB (default) | 10,000 | 10,000 | 10,000 | 0.442 + 0.116 | 45.46 / 57.26 / 57.27 (10,000) | Passed | [112500858287](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112500858287) |
| 10,000 | Burst | 11,000 / 256 MiB | 10,000 | 10,000 | 10,000 | 0.474 | 49.47 / 61.18 / 61.21 (10,000) | Passed | [112509307852](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112509307852) |
| 20,000 | Burst | 22,000 / 256 MiB | 20,000 | 20,000 | 20,000 | 0.950 | 59.15 / 91.16 / 91.38 (20,000) | Passed | [112517391792](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112517391792) |

In the failed default-pool burst, 989 submissions were rejected at pool entry (`1016`, pool limit) and 818 watches were dropped. Reconciliation on 7 October 2026 found all 818 dropped transactions in saved canonical, finalized blocks 173195–173198, with `System.ExtrinsicSuccess` and `Coinage.CoinTransferred`. None of the 989 rejected transactions appears in a saved block. Finality stays on the original 8,193 timed transfers. The one-transfer smoke passed ([job 112430856228](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112430856228)).

## Free-quota and offboarding measurements

Both cases are single, independent runs of 100 unloads on the default pool, at test commit [`37b02ba65a52`](https://github.com/paritytech/polkadot-pop-e2e/commit/37b02ba65a52370e64c91b6809e1f2258ce48d55). Proof time is client preparation before release; it is not part of finality. Proof percentiles are nearest-rank over 100 proofs of each kind.

| Case / run | People / unloads | Setup top-ups | Receipt-verified | Finality p50 / p95 / max (N) | Recycler proof p50 / max | Free-token proof p50 / max | Result |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| [Quota 100, default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37570768389/attempts/1) | 1 / 100 | 100 / 100 finalized | 100 | 43.08 / 55.02 / 55.02 (100) | 1.406 / 1.455 | 0.786 / 0.835 | Passed; preliminary |
| [Offboarding 100, default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37590878841/attempts/1) | 100 / 100 | 100 / 100 finalized | 100 | 49.16 / 61.12 / 61.12 (100) | 1.411 / 1.479 | 0.827 / 0.880 | Passed; preliminary |

The quota case's allowance limit was 1,000, so all 100 requests came from one person. Two negative probes were rejected as designed: a reused token with custom error 57 (`UnloadTokenAlreadyConsumed`) and a counter at the limit with custom error 58 (`UnloadTokenCounterOutOfRange`). Real period rollover was not exercised. Policy rows come from a separate model, not native iOS or Android code.

## Merchant and quota evidence references

Verified locally on 7 October 2026. Selected summaries are in the [remaining-flow evidence folder](evidence/remaining-flow-2026-10-07/SHA256SUMS.txt); they are not the full raw artifacts.

| Case | Run / attempt / job | Test commit | Evidence files | Local verification |
| --- | --- | --- | --- | --- |
| Merchant 100, 1,000, 10,000 paced, 10,000 enlarged, 20,000 enlarged | [37510457575 / 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1); jobs in [Merchant fan-in measurements](#merchant-fan-in-measurements) | [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5) | `claim-burst-summary.json`, `claim-burst-audit.json`, `handoff-verification.txt` per case in [merchant/](evidence/remaining-flow-2026-10-07/merchant/20000-burst-enlarged/handoff-verification.txt) | `verify-remaining-flow.py` recheck, 7 October 2026 |
| Merchant 10,000, default | [37510457575 / 1 / 112493393120](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112493393120) | [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5) | [reconciliation](evidence/remaining-flow-2026-10-07/merchant/10000-burst-default/claim-burst-reconciliation.json), [summary](evidence/remaining-flow-2026-10-07/merchant/10000-burst-default/claim-burst-summary.json), [audit](evidence/remaining-flow-2026-10-07/merchant/10000-burst-default/claim-burst-audit.json) | Offline reconciliation of 818 dropped watches, 7 October 2026 |
| Quota 100, default | [37570768389 / 1 / 112628661431](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37570768389/job/112628661431) | [`37b02ba65a52`](https://github.com/paritytech/polkadot-pop-e2e/commit/37b02ba65a52370e64c91b6809e1f2258ce48d55) | [summary](evidence/remaining-flow-2026-10-07/quota-100/quota-pilot-summary.json), [audit](evidence/remaining-flow-2026-10-07/quota-100/quota-pilot-wave-1-audit.json), [probes](evidence/remaining-flow-2026-10-07/quota-100/quota-pilot-negative-probes.json), [proofs](evidence/remaining-flow-2026-10-07/quota-100/quota-pilot-wave-1-proofs.jsonl) | [Verifier output](evidence/remaining-flow-2026-10-07/quota-100/local-verification.txt), 7 October 2026 |
| Offboarding 100, default | [37590878841 / 1 / 112691846783](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37590878841/job/112691846783) | [`37b02ba65a52`](https://github.com/paritytech/polkadot-pop-e2e/commit/37b02ba65a52370e64c91b6809e1f2258ce48d55) | [summary](evidence/remaining-flow-2026-10-07/offboard-100/offboard-pilot-summary.json), [audit](evidence/remaining-flow-2026-10-07/offboard-100/offboard-pilot-wave-1-audit.json), [proofs](evidence/remaining-flow-2026-10-07/offboard-100/offboard-pilot-wave-1-proofs.jsonl) | [Verifier output](evidence/remaining-flow-2026-10-07/offboard-100/local-verification.txt), 7 October 2026 |
| Setup failures and skipped cases | [37510457575 / 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1) | [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5) | [case ledger](evidence/remaining-flow-2026-10-07/case-ledger-remaining-flow.json) | Job conclusions and stages, 7 October 2026 |
