# ASIACRYPT 2021: Convexity of division property transitions: theory, algorithms and compact models

Supporting code for the ASIACRYPT 2021 paper by Aleksei Udovenko

> [Convexity of division property transitions and CNF/MILP modeling of large S-boxes](https://doi).

([Full version](https://ia.cr/2021/1285)) can be found on eprint.


## Setup

- Can be run on pypy3 or python3 of recent versions (including [SageMath](https://www.sagemath.org/)).
- It is recommended to set up a virtual environment (venv).
- It is recommended to update `pip` with `pip install -U pip`.


Install [swig](http://swig.org/) and [OpenMP](https://www.openmp.org/) using system package manager:

```bash
apt install swig libomp-dev  # ubuntu
```

(optional) Create virtual environment:

```bash
pypy3 -m venv .venv/pypy3
. .venv/pypy3/bin/activate
```


Install packages (later will be available from PyPI):

```bash
pip install packages/justlogs packages/hackycpp packages/optisolveapi
pip install packages/subsets
pip install packages/divprop
```

## Reproducing results from the paper

### Division convex sets sizes for various S-boxes (Table 1)

```bash
python scripts/sbox_convex_partition.py  # (verbose)
python scripts/sbox_convex_partition.py >/dev/null  # (latex source of the table)
```

To include super-sboxes, run beforehand

```bash
# equiv. to
# make ssb

# fast (one key)
python ./scripts/ssb_divcore.py SSB_ZEROKEY_LED
python ./scripts/ssb_divcore.py SSB_ZEROKEY_SKINNY64

# slow
python ./scripts/ssb_divcore.py SSB_SKINNY64
python ./scripts/ssb_divcore.py SSB_LED
python ./scripts/ssb_divcore.py SSB_MIDORI64
```

**Note:** it takes quite some time (up to a day per full Super-Sbox), however 
the final division core is reached after processing a few chunks (a couple of minutes). For experiments,
it should be safe to stop each super-sbox after, say, 1024 keys (8 x 128 chunks).

### LED trail search

**Note:** requires GNU parallel to be installed, and runs in 4 threads.

**Note:** May consume significant amount of RAM on the first run (afterwards, the division core is cached). Reduce the number of threads in the Makefile if needed.

Takes about 16 hours on a 4-core/8-threads Intel(R) Core(TM) i5-10210U CPU. 

Requires [kissat](https://github.com/arminbiere/kissat) solver installed.

```bash
mkdir .cache  # to enable cache of super-sbox data (optional)
make LED
```

The final trails are available in data/LED_trails_I_J_greedy.txt, where I is the index of the input Super-Sbox (0..3), J is ihe index of the output Super-Sbox, i.e. [data/LED_trails_0_0_greedy.txt](data/LED_trails_0_0_greedy.txt) up to [data/LED_trails_3_3_greedy.txt](data/LED_trails_3_3_greedy.txt).
The format is one trail per line: (not u) v state0 state1 state2 state3 state4 state5. The state transitions are
SR.MC.SR, Super-Sbox, SR.MC.SR, Super-Sbox, SR.MC.SR (external Super-Sboxes are implicit).


### LED trail verification

**Note:** requires GNU parallel to be installed, and runs in 4 threads.

**Note:** May consume significant amount of RAM on the first run (afterwards, the division core is cached). Reduce the number of threads in the Makefile if needed.

Takes about 5 minutes per input/output Super-Sbox combination. (20 minutes total in 4 threads, excluding warmup computations)

```bash
mkdir .cache  # to enable cache of super-sbox data (optional)
make LED_verify
```


### Random 32-bit S-box model

Tool `divprop.random_sbox_benchmark` is installed by pip and can be used to benchmark the advanced algorithm for division core computation.

```bash
# up to 16-bit S-boxes are checked against basic algorithm
time divprop.random_sbox_benchmark 16
...
00:00:00.544 INFO divprop.tool_random_sbox_benchmark:RandomSboxBenchmark: divcore: 720 elements, saving to divcore_random/16/divcore.txt.gz ...
00:00:00.545 INFO divprop.tool_random_sbox_benchmark:RandomSboxBenchmark: lb: 336 elements, saving to divcore_random/16/lb.txt.gz ...
00:00:00.546 INFO divprop.tool_random_sbox_benchmark:RandomSboxBenchmark: ub: 2846 elements, saving to divcore_random/16/ub.txt.gz ...
00:00:00.575 INFO divprop.tool_random_sbox_benchmark:RandomSboxBenchmark: testing...
00:00:26.102 INFO divprop.tool_random_sbox_benchmark:RandomSboxBenchmark: sanity check ok! (n <= 16)
00:00:26.103 INFO divprop.tool_random_sbox_benchmark:RandomSboxBenchmark: finished
________________________________________________________
Executed in   26.67 secs
```

Note that most of the time is spent in the basic algorithm for testing. For example, for 17+ bits there is no sanity testing. n=17 runs in a second.

For 24+ bits S-boxes, specify the `-l` flag which will use filesystem storage for components.

```bash
time divprop.random_sbox_benchmark -l 32
...

```


## Packages overview


### `subsets`

Provides operations on sets of n-bit strings represented densely (bit-packed), including multidimensional transforms and simple bitwise operations. Contains Python bindings to the C++ core. Examples:

```py
from subsets import DenseSet

d = DenseSet(4)  # n=4
d
# <DenseSet hash=35035b6d757eed96 n=4 wt=0 | >

d.add(0b0110)
d.add(0b1011)
d.do_UpperSet()  # in-place
d
# <DenseSet hash=030f7a531e7cb9aa n=4 wt=5 | 2:1 3:3 4:1>
d.to_Bins()
# [Bin(0b0110, n=4), Bin(0b0111, n=4), Bin(0b1011, n=4), Bin(0b1110, n=4), Bin(0b1111, n=4)]

d.MinSet()
# <DenseSet hash=7594984eab0754a0 n=4 wt=2 | 2:1 3:1>
d.MinSet().to_Bins()
# [Bin(0b0110, n=4), Bin(0b1011, n=4)]
```

More information in [./packages/subsets/](./packages/subsets/).


### `divprop`

DivProp is the main package related to the paper's developments on division property. The two most important classes are `Sbox` and `SboxDivision`.

- `Sbox` is a small wrapper for representing S-boxes. 
- `SboxDivision` allows to easily compute all the convex sets described in the paper.

Examples:

```py
from divprop.all_sboxes import AES
from divprop import Sbox, SboxDivision

s = Sbox(AES, 8, 8)
# <Sbox hash=3b66e44419610dd0 n=8 m=8>

sd = SboxDivision(s)
sd.divcore
# <DenseSet hash=14421c71a4b40a67 n=16 wt=122 | 2:25 3:66 4:29 8:2>
sd.min_dppt
# <DenseSet hash=3bdcec9ddb5303f2 n=16 wt=2001 | 0:1 2:64 3:224 4:448 5:560 6:428 7:173 8:54 9:42 10:6 16:1>
sd.invalid_max
# <DenseSet hash=af326bfc6e4b2f4a n=16 wt=87 | 3:30 4:41 7:16>
sd.redundant_min
# <DenseSet hash=d165309d0be60267 n=16 wt=319 | 3:137 4:168 5:6 9:8>
sd.redundant_alternative_min
# <DenseSet hash=82186fa2cffeefc6 n=16 wt=274 | 3:152 4:112 5:2 9:8>
sd.propagation_map
[[0], [1, 2, 4, 8, 16, 32, 64, 128], [1, 2, 4, 8, 16, 32, 64, 128], ..., [4, 10, 18, 24, 33, 40, 48, 65, 80, 98, 129, 144], [255]]
```

The advanced algorithm for heavy S-boxes is implemented in [divprop.divcore_peekanfs](./packages/divprop/src/divprop/divcore_peekanfs.py):

```py
from divprop.divcore_peekanfs import SboxPeekANFs

divcore, invalid_max = SboxPeekANFs(s).compute()
assert divcore == set(sd.divcore.to_Bins())
assert invalid_max == set(sd.invalid_max.to_Bins())
```

Its variation with filesystem cache (to reduce RAM usage) is implemented in [divpop.tool_random_sbox_benchmark](./packages/divprop/src/divprop/tool_random_sbox_benchmark.py)

More information in [./packages/divprop/](./packages/divprop/).


### `optisolveapi`

This package is aiming to provide unified api for SAT and MILP solvers. For now, it provides an API for using external SAT solvers such as [kissat](https://github.com/arminbiere/kissat).

In addition, it provides functions for encoding various constraints (sequential counters, convex encodings, etc.).



## Citation

```tex
@inproceedings{AC:Udo21,
  author    = {Aleksei Udovenko},
  title     = {Convexity of division property transitions: theory, algorithms and compact models},
  booktitle = {{Advances in Cryptology -- ASIACRYPT 2021}},
  series    = {Lecture Notes in Computer Science},
  volume    = {?},
  publisher = {{Springer International Publishing}},
  year      = {2021},
  doi       = {?},
  isbn      = {},
  note      = {to appear}
}
```
