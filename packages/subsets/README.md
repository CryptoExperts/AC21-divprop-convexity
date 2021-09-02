# subsets - binary/box subsets & transforms

This package provides C++ implementation and Python bindings (SWIG) for dense binary/box multidimensional transformations.

Example of such transform is the TruthTable-to-AlgebraicNormalForm conversion (the Möbius transform), TruthTable-to-ParitySet conversion, Lower/UpperClosure with respect to the product partial order, etc. For more details, see Section 5 of ???

Box here means a set of the shape `{0,...d_1} × {0,...d_2} x ...`.


## Installation

```bash
apt install swig  # or any other package manager
pip install hackycpp
pip install subsets
```

Note: the build can take a few minutes.


## Examples

Note: `subsets` uses [binteger](https://binteger.readthedocs.io/) for convenient representations of bit vectors.

See also [tests](tests/) for more examples.


### DenseSet

`DenseSet` stores a subset of n-bit vectors as a bitstring of 2^n bits. 

```python
from subsets import DenseSet

# set of 3-bit vectors
b = DenseSet(3, [6, 7]) 
b
# <DenseSet hash=f502ae1f64521d04 n=3 wt=2 | 2:1 3:1>

list(b)
# [6, 7]

b.to_Bins()
# [Bin(0b110, n=3), Bin(0b111, n=3)]

b.Mobius().to_Bins()
# [Bin(0b110, n=3)] = x0x1

DenseSet(3, [3]).LowerSet().to_Bins()
# [Bin(0b000, n=3), Bin(0b001, n=3), Bin(0b010, n=3), Bin(0b011, n=3)]

DenseSet(3, [3]).LowerSet().MaxSet().to_Bins()
# [Bin(0b011, n=3)]
```

Bitwise operations such as `^,|,&` are supported naturally:

```python
from subsets import DenseSet

list(DenseSet(3, [0, 1]) ^ DenseSet(3, [1, 7]))
# [0, 7]

list(DenseSet(3, [0, 1, 2]).Complement())
# [3, 4, 5, 6, 7]

list(DenseSet(3, [0, 1, 2]).Not())  # equiv. to xor 0xfff... each index set
# [5, 6, 7]

list(DenseSet(3, [0, 1, 2]).Not(3))  # equiv. to xor 3 each index set
# [1, 2, 3]
```

### DenseBox

`DenseBox` stores a subset of a set `{0,...d_1} × {0,...d_2} × ...` as a bitstring of length `(d_1 + 1) × (d_2 + 1) × ...`. It supports multidimensional transforsms similar to `DenseSet`.

Each element is addressed either by a list of integers from `{0,...d_1} × {0,...d_2} × ...`, or by a packed 64-bit integer.

```python
from subsets import DenseBox

d = DenseBox([2, 3, 4])  # dimensions
d.data.n
# 60 = 3*4*5 bits to stored d

d.set(d.pack([1, 0, 3]))
assert [1, 0, 3] in d
assert [0, 0, 0] not in d

d
# <DenseBox(2,3,4) hash=89366ea36f16f570 wt=1 | 4:1>

list(d.LowerSet())
# [0, 1, 2, 3, 20, 21, 22, 23]

d.LowerSet().get_unpacked()
# ((0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3))
```

In addition, `DenseBox` can be converted to and from `DenseSet` with `n = d_1 + d_2 + ...`:
the first produces set of bitstrings that have weight pattern `(l_1, l_2, ...)` for each such pattern in the given `DenseBox` (expansion);
the second produces all weight patterns in a given `DenseSet` (compression):

```python
from subsets import DenseSet

d = DenseSet(4, [1, 2, 3, 12]).to_DenseBox([2, 2])

d.get_unpacked()
# ((0, 1), (0, 2), (2, 0))
```

**Caution:** a convex binary set may have a non-convex weight pattern bounds:

```python
from subsets import DenseSet

d = DenseSet(4, [7, 8])
d.to_Bins()
# [Bin(0b0111, n=4), Bin(0b1000, n=4)]

d == d.LowerSet() & d.UpperSet()
# True  - is convex

db = d.to_DenseBox([4])
db
# <DenseBox(4) hash=ef70011e9740ac1c wt=2 | 1:1 3:1>

db.LowerSet() & db.UpperSet()  # convex hull
# <DenseBox(4) hash=c3729f500963e25a wt=3 | 1:1 2:1 3:1>

db == db.LowerSet() & db.UpperSet()
# False - obviously non-convex
```

### Division Property Propagation Table

Basic implementation of the (reduced) DPPT computation algorithm (Section 5 of ???).

```python
from subsets import DenseSet

sbox = [  # AES
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

graph = DenseSet(16)
for x, y in enumerate(sbox):
    graph.set((x << 8) | y)

# do_* does the operation in place
dppt = graph
dppt.do_ParitySet()  # same as dppt.do_Sweep_XOR_down()
dppt.do_UpperSet(0xff00)
dppt.do_MinSet(0x00ff)
dppt.do_Not(0xff00)

[v.split(2) for v in dppt.to_Bins()]
# (Bin(0b00000000, n=8), Bin(0b00000000, n=8))
# (Bin(0b00000001, n=8), Bin(0b00000001, n=8))
# (Bin(0b00000001, n=8), Bin(0b00000010, n=8))
# (Bin(0b00000001, n=8), Bin(0b00000100, n=8))
# (Bin(0b00000001, n=8), Bin(0b00001000, n=8))
# (Bin(0b00000001, n=8), Bin(0b00010000, n=8))
# (Bin(0b00000001, n=8), Bin(0b00100000, n=8))
# (Bin(0b00000001, n=8), Bin(0b01000000, n=8))
# (Bin(0b00000001, n=8), Bin(0b10000000, n=8))
# (Bin(0b00000010, n=8), Bin(0b00000001, n=8))
# (Bin(0b00000010, n=8), Bin(0b00000010, n=8))
# (Bin(0b00000010, n=8), Bin(0b00000100, n=8))
# (Bin(0b00000010, n=8), Bin(0b00001000, n=8))
# ...
# (Bin(0b11111101, n=8), Bin(0b10000000, n=8))
# (Bin(0b11111110, n=8), Bin(0b00000100, n=8))
# (Bin(0b11111110, n=8), Bin(0b00001010, n=8))
# (Bin(0b11111110, n=8), Bin(0b00010010, n=8))
# (Bin(0b11111110, n=8), Bin(0b00011000, n=8))
# (Bin(0b11111110, n=8), Bin(0b00100001, n=8))
# (Bin(0b11111110, n=8), Bin(0b00101000, n=8))
# (Bin(0b11111110, n=8), Bin(0b00110000, n=8))
# (Bin(0b11111110, n=8), Bin(0b01000001, n=8))
# (Bin(0b11111110, n=8), Bin(0b01010000, n=8))
# (Bin(0b11111110, n=8), Bin(0b01100010, n=8))
# (Bin(0b11111110, n=8), Bin(0b10000001, n=8))
# (Bin(0b11111110, n=8), Bin(0b10010000, n=8))
# (Bin(0b11111111, n=8), Bin(0b11111111, n=8))
```

### Extra

Subsets can be stored to / loaded from files, and a command line tool to view information on such files is provided:

```bash
$ subsets.info -s data/sbox_aes/ddt.set
INFO:subsets.setinfo:data/sbox_aes/ddt.set: <DenseSet hash=3ab8d88c8de49448 n=16 wt=32386 | 0:1 2:24 3:212 4:855 5:2205 6:3901 7:5637 8:6378 9:5746 10:4007 11:2169 12:907 13:276 14:58 15:9 16:1>

$ subsets.info data/sbox_aes/ddt.set
INFO:subsets.setinfo:set file data/sbox_aes/ddt.set
INFO:subsets.setinfo:data/sbox_aes/ddt.set: <DenseSet hash=3ab8d88c8de49448 n=16 wt=32386 | 0:1 2:24 3:212 4:855 5:2205 6:3901 7:5637 8:6378 9:5746 10:4007 11:2169 12:907 13:276 14:58 15:9 16:1>
INFO:subsets.setinfo:stat by weights:
INFO:subsets.setinfo:0 : 1
INFO:subsets.setinfo:1 : 0
INFO:subsets.setinfo:2 : 24
INFO:subsets.setinfo:3 : 212
INFO:subsets.setinfo:4 : 855
INFO:subsets.setinfo:5 : 2205
INFO:subsets.setinfo:6 : 3901
INFO:subsets.setinfo:7 : 5637
INFO:subsets.setinfo:8 : 6378
INFO:subsets.setinfo:9 : 5746
INFO:subsets.setinfo:10 : 4007
INFO:subsets.setinfo:11 : 2169
INFO:subsets.setinfo:12 : 907
INFO:subsets.setinfo:13 : 276
INFO:subsets.setinfo:14 : 58
INFO:subsets.setinfo:15 : 9
INFO:subsets.setinfo:16 : 1
INFO:subsets.setinfo:stat by pairs:
INFO:subsets.setinfo:0 0 : 1
INFO:subsets.setinfo:1 1 : 24
INFO:subsets.setinfo:1 2 : 102
INFO:subsets.setinfo:1 3 : 234
...
INFO:subsets.setinfo:8 6 : 14
INFO:subsets.setinfo:8 7 : 5
INFO:subsets.setinfo:8 8 : 1
INFO:subsets.setinfo:
```