"""
Part of the S-box collection by Léo Perrin, see
https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/sboxes.html
"""

from divprop import Sbox

AES = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x1, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x4, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x5, 0x9a, 0x7, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x9, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x0, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x2, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0xc, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0xb, 0xdb, 0xe0, 0x32, 0x3a, 0xa, 0x49, 0x6, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x8, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x3, 0xf6, 0xe, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1, 0x89, 0xd, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0xf, 0xb0, 0x54, 0xbb, 0x16]
APN_6 = [0x0, 0x36, 0x30, 0xd, 0xf, 0x12, 0x35, 0x23, 0x19, 0x3f, 0x2d, 0x34, 0x3, 0x14, 0x29, 0x21, 0x3b, 0x24, 0x2, 0x22, 0xa, 0x8, 0x39, 0x25, 0x3c, 0x13, 0x2a, 0xe, 0x32, 0x1a, 0x3a, 0x18, 0x27, 0x1b, 0x15, 0x11, 0x10, 0x1d, 0x1, 0x3e, 0x2f, 0x28, 0x33, 0x38, 0x7, 0x2b, 0x2c, 0x26, 0x1f, 0xb, 0x4, 0x1c, 0x3d, 0x2e, 0x5, 0x31, 0x9, 0x6, 0x17, 0x20, 0x1e, 0xc, 0x37, 0x16]
Ascon = [0x4, 0xb, 0x1f, 0x14, 0x1a, 0x15, 0x9, 0x2, 0x1b, 0x5, 0x8, 0x12, 0x1d, 0x3, 0x6, 0x1c, 0x1e, 0x13, 0x7, 0xe, 0x0, 0xd, 0x11, 0x18, 0x10, 0xc, 0x1, 0x19, 0x16, 0xa, 0xf, 0x17]
DryGASCON128 = [0x4, 0xf, 0x1b, 0x1, 0xb, 0x0, 0x17, 0xd, 0x1f, 0x1c, 0x2, 0x10, 0x12, 0x11, 0xc, 0x1e, 0x1a, 0x19, 0x14, 0x6, 0x15, 0x16, 0x18, 0xa, 0x5, 0xe, 0x9, 0x13, 0x8, 0x3, 0x7, 0x1d]
DryGASCON256 = [0x10, 0x93, 0x11f, 0x9d, 0x1f, 0x9c, 0x113, 0x91, 0x2a, 0xa9, 0x127, 0xa5, 0x27, 0xa4, 0x129, 0xab, 0x2c, 0xaf, 0x123, 0xa1, 0x23, 0xa0, 0x12f, 0xad, 0x1a, 0x99, 0x117, 0x95, 0x17, 0x94, 0x119, 0x9b, 0xf8, 0x7b, 0x1f7, 0x75, 0xf7, 0x74, 0x1fb, 0x79, 0xca, 0x49, 0x1c7, 0x45, 0xc7, 0x44, 0x1c9, 0x4b, 0xcc, 0x4f, 0x1c3, 0x41, 0xc3, 0x40, 0x1cf, 0x4d, 0xf2, 0x71, 0x1ff, 0x7d, 0xff, 0x7c, 0x1f1, 0x73, 0xe0, 0x63, 0x1ef, 0x6d, 0xef, 0x6c, 0x1e3, 0x61, 0xda, 0x59, 0x1d7, 0x55, 0xd7, 0x54, 0x1d9, 0x5b, 0xdc, 0x5f, 0x1d3, 0x51, 0xd3, 0x50, 0x1df, 0x5d, 0xea, 0x69, 0x1e7, 0x65, 0xe7, 0x64, 0x1e9, 0x6b, 0x38, 0xbb, 0x137, 0xb5, 0x37, 0xb4, 0x13b, 0xb9, 0xa, 0x89, 0x107, 0x85, 0x7, 0x84, 0x109, 0x8b, 0xc, 0x8f, 0x103, 0x81, 0x3, 0x80, 0x10f, 0x8d, 0x32, 0xb1, 0x13f, 0xbd, 0x3f, 0xbc, 0x131, 0xb3, 0x1b1, 0x1b2, 0xbe, 0x1bc, 0x1be, 0x1bd, 0xb2, 0x1b0, 0x18b, 0x188, 0x86, 0x184, 0x186, 0x185, 0x88, 0x18a, 0x18d, 0x18e, 0x82, 0x180, 0x182, 0x181, 0x8e, 0x18c, 0x1bb, 0x1b8, 0xb6, 0x1b4, 0x1b6, 0x1b5, 0xb8, 0x1ba, 0x179, 0x17a, 0x76, 0x174, 0x176, 0x175, 0x7a, 0x178, 0x14b, 0x148, 0x46, 0x144, 0x146, 0x145, 0x48, 0x14a, 0x14d, 0x14e, 0x42, 0x140, 0x142, 0x141, 0x4e, 0x14c, 0x173, 0x170, 0x7e, 0x17c, 0x17e, 0x17d, 0x70, 0x172, 0x161, 0x162, 0x6e, 0x16c, 0x16e, 0x16d, 0x62, 0x160, 0x15b, 0x158, 0x56, 0x154, 0x156, 0x155, 0x58, 0x15a, 0x15d, 0x15e, 0x52, 0x150, 0x152, 0x151, 0x5e, 0x15c, 0x16b, 0x168, 0x66, 0x164, 0x166, 0x165, 0x68, 0x16a, 0x199, 0x19a, 0x96, 0x194, 0x196, 0x195, 0x9a, 0x198, 0x1ab, 0x1a8, 0xa6, 0x1a4, 0x1a6, 0x1a5, 0xa8, 0x1aa, 0x1ad, 0x1ae, 0xa2, 0x1a0, 0x1a2, 0x1a1, 0xae, 0x1ac, 0x193, 0x190, 0x9e, 0x19c, 0x19e, 0x19d, 0x90, 0x192, 0x1d2, 0x1d1, 0x1d, 0xde, 0x1dd, 0x1de, 0x1d, 0xd2, 0x1e8, 0x1eb, 0x1e, 0xe6, 0x1e5, 0x1e6, 0x1e, 0xe8, 0x1ee, 0x1ed, 0x1e, 0xe2, 0x1e1, 0x1e2, 0x1e, 0xee, 0x1d8, 0x1db, 0x1d, 0xd6, 0x1d5, 0x1d6, 0x1d, 0xd8, 0x13a, 0x139, 0x13, 0x36, 0x135, 0x136, 0x13, 0x3a, 0x108, 0x10b, 0x10, 0x6, 0x105, 0x106, 0x10, 0x8, 0x10e, 0x10d, 0x10, 0x2, 0x101, 0x102, 0x10, 0xe, 0x130, 0x133, 0x13, 0x3e, 0x13d, 0x13e, 0x13, 0x30, 0x122, 0x121, 0x12, 0x2e, 0x12d, 0x12e, 0x12, 0x22, 0x118, 0x11b, 0x11, 0x16, 0x115, 0x116, 0x11, 0x18, 0x11e, 0x11d, 0x11, 0x12, 0x111, 0x112, 0x11, 0x1e, 0x128, 0x12b, 0x12, 0x26, 0x125, 0x126, 0x12, 0x28, 0x1fa, 0x1f9, 0x1f, 0xf6, 0x1f5, 0x1f6, 0x1f, 0xfa, 0x1c8, 0x1cb, 0x1c, 0xc6, 0x1c5, 0x1c6, 0x1c, 0xc8, 0x1ce, 0x1cd, 0x1c, 0xc2, 0x1c1, 0x1c2, 0x1c, 0xce, 0x1f0, 0x1f3, 0x1f, 0xfe, 0x1fd, 0x1fe, 0x1f, 0xf0, 0x33, 0xb0, 0x3d, 0x1bf, 0x3c, 0xbf, 0x31, 0x1b3, 0x9, 0x8a, 0x5, 0x187, 0x4, 0x87, 0xb, 0x189, 0xf, 0x8c, 0x1, 0x183, 0x0, 0x83, 0xd, 0x18f, 0x39, 0xba, 0x35, 0x1b7, 0x34, 0xb7, 0x3b, 0x1b9, 0xfb, 0x78, 0xf5, 0x177, 0xf4, 0x77, 0xf9, 0x17b, 0xc9, 0x4a, 0xc5, 0x147, 0xc4, 0x47, 0xcb, 0x149, 0xcf, 0x4c, 0xc1, 0x143, 0xc0, 0x43, 0xcd, 0x14f, 0xf1, 0x72, 0xfd, 0x17f, 0xfc, 0x7f, 0xf3, 0x171, 0xe3, 0x60, 0xed, 0x16f, 0xec, 0x6f, 0xe1, 0x163, 0xd9, 0x5a, 0xd5, 0x157, 0xd4, 0x57, 0xdb, 0x159, 0xdf, 0x5c, 0xd1, 0x153, 0xd0, 0x53, 0xdd, 0x15f, 0xe9, 0x6a, 0xe5, 0x167, 0xe4, 0x67, 0xeb, 0x169, 0x1b, 0x98, 0x15, 0x197, 0x14, 0x97, 0x19, 0x19b, 0x29, 0xaa, 0x25, 0x1a7, 0x24, 0xa7, 0x2b, 0x1a9, 0x2f, 0xac, 0x21, 0x1a3, 0x20, 0xa3, 0x2d, 0x1af, 0x11, 0x92, 0x1d, 0x19f, 0x1c, 0x9f, 0x13, 0x191]
Fides_5 = [0x1, 0x0, 0x19, 0x1a, 0x11, 0x1d, 0x15, 0x1b, 0x14, 0x5, 0x4, 0x17, 0xe, 0x12, 0x2, 0x1c, 0xf, 0x8, 0x6, 0x3, 0xd, 0x7, 0x18, 0x10, 0x1e, 0x9, 0x1f, 0xa, 0x16, 0xc, 0xb, 0x13]
Fides_6 = [0x36, 0x0, 0x30, 0xd, 0xf, 0x12, 0x23, 0x35, 0x3f, 0x19, 0x2d, 0x34, 0x3, 0x14, 0x21, 0x29, 0x8, 0xa, 0x39, 0x25, 0x3b, 0x24, 0x22, 0x2, 0x1a, 0x32, 0x3a, 0x18, 0x3c, 0x13, 0xe, 0x2a, 0x2e, 0x3d, 0x5, 0x31, 0x1f, 0xb, 0x1c, 0x4, 0xc, 0x1e, 0x37, 0x16, 0x9, 0x6, 0x20, 0x17, 0x1b, 0x27, 0x15, 0x11, 0x10, 0x1d, 0x3e, 0x1, 0x28, 0x2f, 0x33, 0x38, 0x7, 0x2b, 0x26, 0x2c]
GIFT = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
Iceberg = [0x24, 0xc1, 0x38, 0x30, 0xe7, 0x57, 0xdf, 0x20, 0x3e, 0x99, 0x1a, 0x34, 0xca, 0xd6, 0x52, 0xfd, 0x40, 0x6c, 0xd3, 0x3d, 0x4a, 0x59, 0xf8, 0x77, 0xfb, 0x61, 0xa, 0x56, 0xb9, 0xd2, 0xfc, 0xf1, 0x7, 0xf5, 0x93, 0xcd, 0x0, 0xb6, 0x62, 0xa7, 0x63, 0xfe, 0x44, 0xbd, 0x5f, 0x92, 0x6b, 0x68, 0x3, 0x4e, 0xa2, 0x97, 0xb, 0x60, 0x83, 0xa3, 0x2, 0xe5, 0x45, 0x67, 0xf4, 0x13, 0x8, 0x8b, 0x10, 0xce, 0xbe, 0xb4, 0x2a, 0x3a, 0x96, 0x84, 0xc8, 0x9f, 0x14, 0xc0, 0xc4, 0x6f, 0x31, 0xd9, 0xab, 0xae, 0xe, 0x64, 0x7c, 0xda, 0x1b, 0x5, 0xa8, 0x15, 0xa5, 0x90, 0x94, 0x85, 0x71, 0x2c, 0x35, 0x19, 0x26, 0x28, 0x53, 0xe2, 0x7f, 0x3b, 0x2f, 0xa9, 0xcc, 0x2e, 0x11, 0x76, 0xed, 0x4d, 0x87, 0x5e, 0xc2, 0xc7, 0x80, 0xb0, 0x6d, 0x17, 0xb2, 0xff, 0xe4, 0xb7, 0x54, 0x9d, 0xb8, 0x66, 0x74, 0x9c, 0xdb, 0x36, 0x47, 0x5d, 0xde, 0x70, 0xd5, 0x91, 0xaa, 0x3f, 0xc9, 0xd8, 0xf3, 0xf2, 0x5b, 0x89, 0x2d, 0x22, 0x5c, 0xe1, 0x46, 0x33, 0xe6, 0x9, 0xbc, 0xe8, 0x81, 0x7d, 0xe9, 0x49, 0xe0, 0xb1, 0x32, 0x37, 0xea, 0x5a, 0xf6, 0x27, 0x58, 0x69, 0x8a, 0x50, 0xba, 0xdd, 0x51, 0xf9, 0x75, 0xa1, 0x78, 0xd0, 0x43, 0xf7, 0x25, 0x7b, 0x7e, 0x1c, 0xac, 0xd4, 0x9a, 0x2b, 0x42, 0xe3, 0x4b, 0x1, 0x72, 0xd7, 0x4c, 0xfa, 0xeb, 0x73, 0x48, 0x8c, 0xc, 0xf0, 0x6a, 0x23, 0x41, 0xec, 0xb3, 0xef, 0x1d, 0x12, 0xbb, 0x88, 0xd, 0xc3, 0x8d, 0x4f, 0x55, 0x82, 0xee, 0xad, 0x86, 0x6, 0xa0, 0x95, 0x65, 0xbf, 0x7a, 0x39, 0x98, 0x4, 0x9b, 0x9e, 0xa4, 0xc6, 0xcf, 0x6e, 0xdc, 0xd1, 0xcb, 0x1f, 0x8f, 0x8e, 0x3c, 0x21, 0xa6, 0xb5, 0x16, 0xaf, 0xc5, 0x18, 0x1e, 0xf, 0x29, 0x79]
KLEIN = [0x7, 0x4, 0xa, 0x9, 0x1, 0xf, 0xb, 0x0, 0xc, 0x3, 0x2, 0x6, 0x8, 0xe, 0xd, 0x5]
KNOT = [0x4, 0x0, 0xa, 0x7, 0xb, 0xe, 0x1, 0xd, 0x9, 0xf, 0x6, 0x8, 0x5, 0x2, 0xc, 0x3]
Kuznyechik = [0xfc, 0xee, 0xdd, 0x11, 0xcf, 0x6e, 0x31, 0x16, 0xfb, 0xc4, 0xfa, 0xda, 0x23, 0xc5, 0x4, 0x4d, 0xe9, 0x77, 0xf0, 0xdb, 0x93, 0x2e, 0x99, 0xba, 0x17, 0x36, 0xf1, 0xbb, 0x14, 0xcd, 0x5f, 0xc1, 0xf9, 0x18, 0x65, 0x5a, 0xe2, 0x5c, 0xef, 0x21, 0x81, 0x1c, 0x3c, 0x42, 0x8b, 0x1, 0x8e, 0x4f, 0x5, 0x84, 0x2, 0xae, 0xe3, 0x6a, 0x8f, 0xa0, 0x6, 0xb, 0xed, 0x98, 0x7f, 0xd4, 0xd3, 0x1f, 0xeb, 0x34, 0x2c, 0x51, 0xea, 0xc8, 0x48, 0xab, 0xf2, 0x2a, 0x68, 0xa2, 0xfd, 0x3a, 0xce, 0xcc, 0xb5, 0x70, 0xe, 0x56, 0x8, 0xc, 0x76, 0x12, 0xbf, 0x72, 0x13, 0x47, 0x9c, 0xb7, 0x5d, 0x87, 0x15, 0xa1, 0x96, 0x29, 0x10, 0x7b, 0x9a, 0xc7, 0xf3, 0x91, 0x78, 0x6f, 0x9d, 0x9e, 0xb2, 0xb1, 0x32, 0x75, 0x19, 0x3d, 0xff, 0x35, 0x8a, 0x7e, 0x6d, 0x54, 0xc6, 0x80, 0xc3, 0xbd, 0xd, 0x57, 0xdf, 0xf5, 0x24, 0xa9, 0x3e, 0xa8, 0x43, 0xc9, 0xd7, 0x79, 0xd6, 0xf6, 0x7c, 0x22, 0xb9, 0x3, 0xe0, 0xf, 0xec, 0xde, 0x7a, 0x94, 0xb0, 0xbc, 0xdc, 0xe8, 0x28, 0x50, 0x4e, 0x33, 0xa, 0x4a, 0xa7, 0x97, 0x60, 0x73, 0x1e, 0x0, 0x62, 0x44, 0x1a, 0xb8, 0x38, 0x82, 0x64, 0x9f, 0x26, 0x41, 0xad, 0x45, 0x46, 0x92, 0x27, 0x5e, 0x55, 0x2f, 0x8c, 0xa3, 0xa5, 0x7d, 0x69, 0xd5, 0x95, 0x3b, 0x7, 0x58, 0xb3, 0x40, 0x86, 0xac, 0x1d, 0xf7, 0x30, 0x37, 0x6b, 0xe4, 0x88, 0xd9, 0xe7, 0x89, 0xe1, 0x1b, 0x83, 0x49, 0x4c, 0x3f, 0xf8, 0xfe, 0x8d, 0x53, 0xaa, 0x90, 0xca, 0xd8, 0x85, 0x61, 0x20, 0x71, 0x67, 0xa4, 0x2d, 0x2b, 0x9, 0x5b, 0xcb, 0x9b, 0x25, 0xd0, 0xbe, 0xe5, 0x6c, 0x52, 0x59, 0xa6, 0x74, 0xd2, 0xe6, 0xf4, 0xb4, 0xc0, 0xd1, 0x66, 0xaf, 0xc2, 0x39, 0x4b, 0x63, 0xb6]
MIBS = [0x4, 0xf, 0x3, 0x8, 0xd, 0xa, 0xc, 0x0, 0xb, 0x5, 0x7, 0xe, 0x2, 0x6, 0x1, 0x9]
Midori_MC_slice = [0x0, 0xe, 0xd, 0x3, 0xb, 0x5, 0x6, 0x8, 0x7, 0x9, 0xa, 0x4, 0xc, 0x2, 0x1, 0xf]
Midori_Sb0 = [0xc, 0xa, 0xd, 0x3, 0xe, 0xb, 0xf, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]
Midori_Sb1 = [0x1, 0x0, 0x5, 0x3, 0xe, 0x2, 0xf, 0x7, 0xd, 0xa, 0x9, 0xb, 0xc, 0x8, 0x4, 0x6]
Noekeon = [0x7, 0xa, 0x2, 0xc, 0x4, 0x8, 0xf, 0x0, 0x5, 0x9, 0x1, 0xe, 0x3, 0xd, 0xb, 0x6]
PRESENT = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
PRESENTMOD = [0x6, 0x7, 0xe, 0x3, 0x1, 0x0, 0x8, 0xd, 0x9, 0x4, 0xf, 0xa, 0xc, 0x5, 0xb, 0x2]
PRINCE = [0xb, 0xf, 0x3, 0x2, 0xa, 0xc, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xe, 0x5, 0xd, 0x4]
PRINTcipher = [0x0, 0x1, 0x3, 0x6, 0x7, 0x4, 0x5, 0x2]
Panda = [0x0, 0x1, 0x3, 0x2, 0xf, 0xc, 0x9, 0xb, 0xa, 0x6, 0x8, 0x7, 0x5, 0xe, 0xd, 0x4]
Piccolo = [0xe, 0x4, 0xb, 0x2, 0x3, 0x8, 0x0, 0x9, 0x1, 0xa, 0x7, 0xf, 0x6, 0xc, 0x5, 0xd]
Pride = [0x0, 0x4, 0x8, 0xf, 0x1, 0x5, 0xe, 0x9, 0x2, 0x7, 0xa, 0xc, 0xb, 0xd, 0x6, 0x3]
Pyjamask_3 = [0x1, 0x3, 0x6, 0x5, 0x2, 0x4, 0x7, 0x0]
Pyjamask_4 = [0x2, 0xd, 0x3, 0x9, 0x7, 0xb, 0xa, 0x6, 0xe, 0x0, 0xf, 0x4, 0x8, 0x5, 0x1, 0xc]
Rectangle = [0x6, 0x5, 0xc, 0xa, 0x1, 0xe, 0x7, 0x9, 0xb, 0x0, 0x3, 0xd, 0x8, 0xf, 0x4, 0x2]
SC2000_4 = [0x2, 0x5, 0xa, 0xc, 0x7, 0xf, 0x1, 0xb, 0xd, 0x6, 0x0, 0x9, 0x4, 0x8, 0x3, 0xe]
SC2000_5 = [0x14, 0x1a, 0x7, 0x1f, 0x13, 0xc, 0xa, 0xf, 0x16, 0x1e, 0xd, 0xe, 0x4, 0x18, 0x9, 0x12, 0x1b, 0xb, 0x1, 0x15, 0x6, 0x10, 0x2, 0x1c, 0x17, 0x5, 0x8, 0x3, 0x0, 0x11, 0x1d, 0x19]
SC2000_6 = [0x2f, 0x3b, 0x19, 0x2a, 0xf, 0x17, 0x1c, 0x27, 0x1a, 0x26, 0x24, 0x13, 0x3c, 0x18, 0x1d, 0x38, 0x25, 0x3f, 0x14, 0x3d, 0x37, 0x2, 0x1e, 0x2c, 0x9, 0xa, 0x6, 0x16, 0x35, 0x30, 0x33, 0xb, 0x3e, 0x34, 0x23, 0x12, 0xe, 0x2e, 0x0, 0x36, 0x11, 0x28, 0x1b, 0x4, 0x1f, 0x8, 0x5, 0xc, 0x3, 0x10, 0x29, 0x22, 0x21, 0x7, 0x2d, 0x31, 0x32, 0x3a, 0x1, 0x15, 0x2b, 0x39, 0x20, 0xd]
SKINNY_4 = [0xc, 0x6, 0x9, 0x0, 0x1, 0xa, 0x2, 0xb, 0x3, 0x8, 0x5, 0xd, 0x4, 0xe, 0x7, 0xf]
SKINNY_8 = [0x65, 0x4c, 0x6a, 0x42, 0x4b, 0x63, 0x43, 0x6b, 0x55, 0x75, 0x5a, 0x7a, 0x53, 0x73, 0x5b, 0x7b, 0x35, 0x8c, 0x3a, 0x81, 0x89, 0x33, 0x80, 0x3b, 0x95, 0x25, 0x98, 0x2a, 0x90, 0x23, 0x99, 0x2b, 0xe5, 0xcc, 0xe8, 0xc1, 0xc9, 0xe0, 0xc0, 0xe9, 0xd5, 0xf5, 0xd8, 0xf8, 0xd0, 0xf0, 0xd9, 0xf9, 0xa5, 0x1c, 0xa8, 0x12, 0x1b, 0xa0, 0x13, 0xa9, 0x5, 0xb5, 0xa, 0xb8, 0x3, 0xb0, 0xb, 0xb9, 0x32, 0x88, 0x3c, 0x85, 0x8d, 0x34, 0x84, 0x3d, 0x91, 0x22, 0x9c, 0x2c, 0x94, 0x24, 0x9d, 0x2d, 0x62, 0x4a, 0x6c, 0x45, 0x4d, 0x64, 0x44, 0x6d, 0x52, 0x72, 0x5c, 0x7c, 0x54, 0x74, 0x5d, 0x7d, 0xa1, 0x1a, 0xac, 0x15, 0x1d, 0xa4, 0x14, 0xad, 0x2, 0xb1, 0xc, 0xbc, 0x4, 0xb4, 0xd, 0xbd, 0xe1, 0xc8, 0xec, 0xc5, 0xcd, 0xe4, 0xc4, 0xed, 0xd1, 0xf1, 0xdc, 0xfc, 0xd4, 0xf4, 0xdd, 0xfd, 0x36, 0x8e, 0x38, 0x82, 0x8b, 0x30, 0x83, 0x39, 0x96, 0x26, 0x9a, 0x28, 0x93, 0x20, 0x9b, 0x29, 0x66, 0x4e, 0x68, 0x41, 0x49, 0x60, 0x40, 0x69, 0x56, 0x76, 0x58, 0x78, 0x50, 0x70, 0x59, 0x79, 0xa6, 0x1e, 0xaa, 0x11, 0x19, 0xa3, 0x10, 0xab, 0x6, 0xb6, 0x8, 0xba, 0x0, 0xb3, 0x9, 0xbb, 0xe6, 0xce, 0xea, 0xc2, 0xcb, 0xe3, 0xc3, 0xeb, 0xd6, 0xf6, 0xda, 0xfa, 0xd3, 0xf3, 0xdb, 0xfb, 0x31, 0x8a, 0x3e, 0x86, 0x8f, 0x37, 0x87, 0x3f, 0x92, 0x21, 0x9e, 0x2e, 0x97, 0x27, 0x9f, 0x2f, 0x61, 0x48, 0x6e, 0x46, 0x4f, 0x67, 0x47, 0x6f, 0x51, 0x71, 0x5e, 0x7e, 0x57, 0x77, 0x5f, 0x7f, 0xa2, 0x18, 0xae, 0x16, 0x1f, 0xa7, 0x17, 0xaf, 0x1, 0xb2, 0xe, 0xbe, 0x7, 0xb7, 0xf, 0xbf, 0xe2, 0xca, 0xee, 0xc6, 0xcf, 0xe7, 0xc7, 0xef, 0xd2, 0xf2, 0xde, 0xfe, 0xd7, 0xf7, 0xdf, 0xff]
SMS4 = [0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x5, 0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x4, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x6, 0x99, 0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0xb, 0x43, 0xed, 0xcf, 0xac, 0x62, 0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x8, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6, 0x47, 0x7, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8, 0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0xf, 0x4b, 0x70, 0x56, 0x9d, 0x35, 0x1e, 0x24, 0xe, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x1, 0x21, 0x78, 0x87, 0xd4, 0x0, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x2, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e, 0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1, 0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3, 0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0xd, 0x53, 0x4e, 0x6f, 0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x3, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51, 0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8, 0xa, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0, 0x89, 0x69, 0x97, 0x4a, 0xc, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x9, 0xc5, 0x6e, 0xc6, 0x84, 0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48]
Scream = [0x20, 0x8d, 0xb2, 0xda, 0x33, 0x35, 0xa6, 0xff, 0x7a, 0x52, 0x6a, 0xc6, 0xa4, 0xa8, 0x51, 0x23, 0xa2, 0x96, 0x30, 0xab, 0xc8, 0x17, 0x14, 0x9e, 0xe8, 0xf3, 0xf8, 0xdd, 0x85, 0xe2, 0x4b, 0xd8, 0x6c, 0x1, 0xe, 0x3d, 0xb6, 0x39, 0x4a, 0x83, 0x6f, 0xaa, 0x86, 0x6e, 0x68, 0x40, 0x98, 0x5f, 0x37, 0x13, 0x5, 0x87, 0x4, 0x82, 0x31, 0x89, 0x24, 0x38, 0x9d, 0x54, 0x22, 0x7b, 0x63, 0xbd, 0x75, 0x2c, 0x47, 0xe9, 0xc2, 0x60, 0x43, 0xac, 0x57, 0xa1, 0x1f, 0x27, 0xe7, 0xad, 0x5c, 0xd2, 0xf, 0x77, 0xfd, 0x8, 0x79, 0x3a, 0x49, 0x5d, 0xed, 0x90, 0x65, 0x7c, 0x56, 0x4f, 0x2e, 0x69, 0xcd, 0x44, 0x3f, 0x62, 0x5b, 0x88, 0x6b, 0xc4, 0x5e, 0x2d, 0x67, 0xb, 0x9f, 0x21, 0x29, 0x2a, 0xd6, 0x7e, 0x74, 0xe0, 0x41, 0x73, 0x50, 0x76, 0x55, 0x97, 0x3c, 0x9, 0x7d, 0x5a, 0x92, 0x70, 0x84, 0xb9, 0x26, 0x34, 0x1d, 0x81, 0x32, 0x2b, 0x36, 0x64, 0xae, 0xc0, 0x0, 0xee, 0x8f, 0xa7, 0xbe, 0x58, 0xdc, 0x7f, 0xec, 0x9b, 0x78, 0x10, 0xcc, 0x2f, 0x94, 0xf1, 0x3b, 0x9c, 0x6d, 0x16, 0x48, 0xb5, 0xca, 0x11, 0xfa, 0xd, 0x8e, 0x7, 0xb1, 0xc, 0x12, 0x28, 0x4c, 0x46, 0xf4, 0x8b, 0xa9, 0xcf, 0xbb, 0x3, 0xa0, 0xfc, 0xef, 0x25, 0x80, 0xf6, 0xb3, 0xba, 0x3e, 0xf7, 0xd5, 0x91, 0xc3, 0x8a, 0xc1, 0x45, 0xde, 0x66, 0xf5, 0xa, 0xc9, 0x15, 0xd9, 0xa3, 0x61, 0x99, 0xb0, 0xe4, 0xd1, 0xfb, 0xd3, 0x4e, 0xbf, 0xd4, 0xd7, 0x71, 0xcb, 0x1e, 0xdb, 0x2, 0x1a, 0x93, 0xea, 0xc5, 0xeb, 0x72, 0xf9, 0x1c, 0xe5, 0xce, 0x4d, 0xf2, 0x42, 0x19, 0xe1, 0xdf, 0x59, 0x95, 0xb7, 0x8c, 0x9a, 0xf0, 0x18, 0xe6, 0xc7, 0xaf, 0xbc, 0xb8, 0xe3, 0x1b, 0xd0, 0xa5, 0x53, 0xb4, 0x6, 0xfe]
Skipjack = [0xa3, 0xd7, 0x9, 0x83, 0xf8, 0x48, 0xf6, 0xf4, 0xb3, 0x21, 0x15, 0x78, 0x99, 0xb1, 0xaf, 0xf9, 0xe7, 0x2d, 0x4d, 0x8a, 0xce, 0x4c, 0xca, 0x2e, 0x52, 0x95, 0xd9, 0x1e, 0x4e, 0x38, 0x44, 0x28, 0xa, 0xdf, 0x2, 0xa0, 0x17, 0xf1, 0x60, 0x68, 0x12, 0xb7, 0x7a, 0xc3, 0xe9, 0xfa, 0x3d, 0x53, 0x96, 0x84, 0x6b, 0xba, 0xf2, 0x63, 0x9a, 0x19, 0x7c, 0xae, 0xe5, 0xf5, 0xf7, 0x16, 0x6a, 0xa2, 0x39, 0xb6, 0x7b, 0xf, 0xc1, 0x93, 0x81, 0x1b, 0xee, 0xb4, 0x1a, 0xea, 0xd0, 0x91, 0x2f, 0xb8, 0x55, 0xb9, 0xda, 0x85, 0x3f, 0x41, 0xbf, 0xe0, 0x5a, 0x58, 0x80, 0x5f, 0x66, 0xb, 0xd8, 0x90, 0x35, 0xd5, 0xc0, 0xa7, 0x33, 0x6, 0x65, 0x69, 0x45, 0x0, 0x94, 0x56, 0x6d, 0x98, 0x9b, 0x76, 0x97, 0xfc, 0xb2, 0xc2, 0xb0, 0xfe, 0xdb, 0x20, 0xe1, 0xeb, 0xd6, 0xe4, 0xdd, 0x47, 0x4a, 0x1d, 0x42, 0xed, 0x9e, 0x6e, 0x49, 0x3c, 0xcd, 0x43, 0x27, 0xd2, 0x7, 0xd4, 0xde, 0xc7, 0x67, 0x18, 0x89, 0xcb, 0x30, 0x1f, 0x8d, 0xc6, 0x8f, 0xaa, 0xc8, 0x74, 0xdc, 0xc9, 0x5d, 0x5c, 0x31, 0xa4, 0x70, 0x88, 0x61, 0x2c, 0x9f, 0xd, 0x2b, 0x87, 0x50, 0x82, 0x54, 0x64, 0x26, 0x7d, 0x3, 0x40, 0x34, 0x4b, 0x1c, 0x73, 0xd1, 0xc4, 0xfd, 0x3b, 0xcc, 0xfb, 0x7f, 0xab, 0xe6, 0x3e, 0x5b, 0xa5, 0xad, 0x4, 0x23, 0x9c, 0x14, 0x51, 0x22, 0xf0, 0x29, 0x79, 0x71, 0x7e, 0xff, 0x8c, 0xe, 0xe2, 0xc, 0xef, 0xbc, 0x72, 0x75, 0x6f, 0x37, 0xa1, 0xec, 0xd3, 0x8e, 0x62, 0x8b, 0x86, 0x10, 0xe8, 0x8, 0x77, 0x11, 0xbe, 0x92, 0x4f, 0x24, 0xc5, 0x32, 0x36, 0x9d, 0xcf, 0xf3, 0xa6, 0xbb, 0xac, 0x5e, 0x6c, 0xa9, 0x13, 0x57, 0x25, 0xb5, 0xe3, 0xbd, 0xa8, 0x3a, 0x1, 0x5, 0x59, 0x2a, 0x46]
TWINE = [0xc, 0x0, 0xf, 0xa, 0x2, 0xb, 0x9, 0x5, 0x8, 0x3, 0xd, 0x7, 0x1, 0xe, 0x6, 0x4]
WAGE = [0x2e, 0x1c, 0x6d, 0x2b, 0x35, 0x7, 0x7f, 0x3b, 0x28, 0x8, 0xb, 0x5f, 0x31, 0x11, 0x1b, 0x4d, 0x6e, 0x54, 0xd, 0x9, 0x1f, 0x45, 0x75, 0x53, 0x6a, 0x5d, 0x61, 0x0, 0x4, 0x78, 0x6, 0x1e, 0x37, 0x6f, 0x2f, 0x49, 0x64, 0x34, 0x7d, 0x19, 0x39, 0x33, 0x43, 0x57, 0x60, 0x62, 0x13, 0x5, 0x77, 0x47, 0x4f, 0x4b, 0x1d, 0x2d, 0x24, 0x48, 0x74, 0x58, 0x25, 0x5e, 0x5a, 0x76, 0x41, 0x42, 0x27, 0x3e, 0x6c, 0x1, 0x2c, 0x3c, 0x4e, 0x1a, 0x21, 0x2a, 0xa, 0x55, 0x3a, 0x38, 0x18, 0x7e, 0xc, 0x63, 0x67, 0x56, 0x50, 0x7c, 0x32, 0x7a, 0x68, 0x2, 0x6b, 0x17, 0x7b, 0x59, 0x71, 0xf, 0x30, 0x10, 0x22, 0x3d, 0x40, 0x69, 0x52, 0x14, 0x36, 0x44, 0x46, 0x3, 0x16, 0x65, 0x66, 0x72, 0x12, 0xe, 0x29, 0x4a, 0x4c, 0x70, 0x15, 0x26, 0x79, 0x51, 0x23, 0x3f, 0x73, 0x5b, 0x20, 0x5c]
Whirlpool = [0x18, 0x23, 0xc6, 0xe8, 0x87, 0xb8, 0x1, 0x4f, 0x36, 0xa6, 0xd2, 0xf5, 0x79, 0x6f, 0x91, 0x52, 0x60, 0xbc, 0x9b, 0x8e, 0xa3, 0xc, 0x7b, 0x35, 0x1d, 0xe0, 0xd7, 0xc2, 0x2e, 0x4b, 0xfe, 0x57, 0x15, 0x77, 0x37, 0xe5, 0x9f, 0xf0, 0x4a, 0xda, 0x58, 0xc9, 0x29, 0xa, 0xb1, 0xa0, 0x6b, 0x85, 0xbd, 0x5d, 0x10, 0xf4, 0xcb, 0x3e, 0x5, 0x67, 0xe4, 0x27, 0x41, 0x8b, 0xa7, 0x7d, 0x95, 0xd8, 0xfb, 0xee, 0x7c, 0x66, 0xdd, 0x17, 0x47, 0x9e, 0xca, 0x2d, 0xbf, 0x7, 0xad, 0x5a, 0x83, 0x33, 0x63, 0x2, 0xaa, 0x71, 0xc8, 0x19, 0x49, 0xd9, 0xf2, 0xe3, 0x5b, 0x88, 0x9a, 0x26, 0x32, 0xb0, 0xe9, 0xf, 0xd5, 0x80, 0xbe, 0xcd, 0x34, 0x48, 0xff, 0x7a, 0x90, 0x5f, 0x20, 0x68, 0x1a, 0xae, 0xb4, 0x54, 0x93, 0x22, 0x64, 0xf1, 0x73, 0x12, 0x40, 0x8, 0xc3, 0xec, 0xdb, 0xa1, 0x8d, 0x3d, 0x97, 0x0, 0xcf, 0x2b, 0x76, 0x82, 0xd6, 0x1b, 0xb5, 0xaf, 0x6a, 0x50, 0x45, 0xf3, 0x30, 0xef, 0x3f, 0x55, 0xa2, 0xea, 0x65, 0xba, 0x2f, 0xc0, 0xde, 0x1c, 0xfd, 0x4d, 0x92, 0x75, 0x6, 0x8a, 0xb2, 0xe6, 0xe, 0x1f, 0x62, 0xd4, 0xa8, 0x96, 0xf9, 0xc5, 0x25, 0x59, 0x84, 0x72, 0x39, 0x4c, 0x5e, 0x78, 0x38, 0x8c, 0xd1, 0xa5, 0xe2, 0x61, 0xb3, 0x21, 0x9c, 0x1e, 0x43, 0xc7, 0xfc, 0x4, 0x51, 0x99, 0x6d, 0xd, 0xfa, 0xdf, 0x7e, 0x24, 0x3b, 0xab, 0xce, 0x11, 0x8f, 0x4e, 0xb7, 0xeb, 0x3c, 0x81, 0x94, 0xf7, 0xb9, 0x13, 0x2c, 0xd3, 0xe7, 0x6e, 0xc4, 0x3, 0x56, 0x44, 0x7f, 0xa9, 0x2a, 0xbb, 0xc1, 0x53, 0xdc, 0xb, 0x9d, 0x6c, 0x31, 0x74, 0xf6, 0x46, 0xac, 0x89, 0x14, 0xe1, 0x16, 0x3a, 0x69, 0x9, 0x70, 0xb6, 0xd0, 0xed, 0xcc, 0x42, 0x98, 0xa4, 0x28, 0x5c, 0xf8, 0x86]
ZUC_S0 = [0x3e, 0x72, 0x5b, 0x47, 0xca, 0xe0, 0x0, 0x33, 0x4, 0xd1, 0x54, 0x98, 0x9, 0xb9, 0x6d, 0xcb, 0x7b, 0x1b, 0xf9, 0x32, 0xaf, 0x9d, 0x6a, 0xa5, 0xb8, 0x2d, 0xfc, 0x1d, 0x8, 0x53, 0x3, 0x90, 0x4d, 0x4e, 0x84, 0x99, 0xe4, 0xce, 0xd9, 0x91, 0xdd, 0xb6, 0x85, 0x48, 0x8b, 0x29, 0x6e, 0xac, 0xcd, 0xc1, 0xf8, 0x1e, 0x73, 0x43, 0x69, 0xc6, 0xb5, 0xbd, 0xfd, 0x39, 0x63, 0x20, 0xd4, 0x38, 0x76, 0x7d, 0xb2, 0xa7, 0xcf, 0xed, 0x57, 0xc5, 0xf3, 0x2c, 0xbb, 0x14, 0x21, 0x6, 0x55, 0x9b, 0xe3, 0xef, 0x5e, 0x31, 0x4f, 0x7f, 0x5a, 0xa4, 0xd, 0x82, 0x51, 0x49, 0x5f, 0xba, 0x58, 0x1c, 0x4a, 0x16, 0xd5, 0x17, 0xa8, 0x92, 0x24, 0x1f, 0x8c, 0xff, 0xd8, 0xae, 0x2e, 0x1, 0xd3, 0xad, 0x3b, 0x4b, 0xda, 0x46, 0xeb, 0xc9, 0xde, 0x9a, 0x8f, 0x87, 0xd7, 0x3a, 0x80, 0x6f, 0x2f, 0xc8, 0xb1, 0xb4, 0x37, 0xf7, 0xa, 0x22, 0x13, 0x28, 0x7c, 0xcc, 0x3c, 0x89, 0xc7, 0xc3, 0x96, 0x56, 0x7, 0xbf, 0x7e, 0xf0, 0xb, 0x2b, 0x97, 0x52, 0x35, 0x41, 0x79, 0x61, 0xa6, 0x4c, 0x10, 0xfe, 0xbc, 0x26, 0x95, 0x88, 0x8a, 0xb0, 0xa3, 0xfb, 0xc0, 0x18, 0x94, 0xf2, 0xe1, 0xe5, 0xe9, 0x5d, 0xd0, 0xdc, 0x11, 0x66, 0x64, 0x5c, 0xec, 0x59, 0x42, 0x75, 0x12, 0xf5, 0x74, 0x9c, 0xaa, 0x23, 0xe, 0x86, 0xab, 0xbe, 0x2a, 0x2, 0xe7, 0x67, 0xe6, 0x44, 0xa2, 0x6c, 0xc2, 0x93, 0x9f, 0xf1, 0xf6, 0xfa, 0x36, 0xd2, 0x50, 0x68, 0x9e, 0x62, 0x71, 0x15, 0x3d, 0xd6, 0x40, 0xc4, 0xe2, 0xf, 0x8e, 0x83, 0x77, 0x6b, 0x25, 0x5, 0x3f, 0xc, 0x30, 0xea, 0x70, 0xb7, 0xa1, 0xe8, 0xa9, 0x65, 0x8d, 0x27, 0x1a, 0xdb, 0x81, 0xb3, 0xa0, 0xf4, 0x45, 0x7a, 0x19, 0xdf, 0xee, 0x78, 0x34, 0x60]
ZUC_S1 = [0x55, 0xc2, 0x63, 0x71, 0x3b, 0xc8, 0x47, 0x86, 0x9f, 0x3c, 0xda, 0x5b, 0x29, 0xaa, 0xfd, 0x77, 0x8c, 0xc5, 0x94, 0xc, 0xa6, 0x1a, 0x13, 0x0, 0xe3, 0xa8, 0x16, 0x72, 0x40, 0xf9, 0xf8, 0x42, 0x44, 0x26, 0x68, 0x96, 0x81, 0xd9, 0x45, 0x3e, 0x10, 0x76, 0xc6, 0xa7, 0x8b, 0x39, 0x43, 0xe1, 0x3a, 0xb5, 0x56, 0x2a, 0xc0, 0x6d, 0xb3, 0x5, 0x22, 0x66, 0xbf, 0xdc, 0xb, 0xfa, 0x62, 0x48, 0xdd, 0x20, 0x11, 0x6, 0x36, 0xc9, 0xc1, 0xcf, 0xf6, 0x27, 0x52, 0xbb, 0x69, 0xf5, 0xd4, 0x87, 0x7f, 0x84, 0x4c, 0xd2, 0x9c, 0x57, 0xa4, 0xbc, 0x4f, 0x9a, 0xdf, 0xfe, 0xd6, 0x8d, 0x7a, 0xeb, 0x2b, 0x53, 0xd8, 0x5c, 0xa1, 0x14, 0x17, 0xfb, 0x23, 0xd5, 0x7d, 0x30, 0x67, 0x73, 0x8, 0x9, 0xee, 0xb7, 0x70, 0x3f, 0x61, 0xb2, 0x19, 0x8e, 0x4e, 0xe5, 0x4b, 0x93, 0x8f, 0x5d, 0xdb, 0xa9, 0xad, 0xf1, 0xae, 0x2e, 0xcb, 0xd, 0xfc, 0xf4, 0x2d, 0x46, 0x6e, 0x1d, 0x97, 0xe8, 0xd1, 0xe9, 0x4d, 0x37, 0xa5, 0x75, 0x5e, 0x83, 0x9e, 0xab, 0x82, 0x9d, 0xb9, 0x1c, 0xe0, 0xcd, 0x49, 0x89, 0x1, 0xb6, 0xbd, 0x58, 0x24, 0xa2, 0x5f, 0x38, 0x78, 0x99, 0x15, 0x90, 0x50, 0xb8, 0x95, 0xe4, 0xd0, 0x91, 0xc7, 0xce, 0xed, 0xf, 0xb4, 0x6f, 0xa0, 0xcc, 0xf0, 0x2, 0x4a, 0x79, 0xc3, 0xde, 0xa3, 0xef, 0xea, 0x51, 0xe6, 0x6b, 0x18, 0xec, 0x1b, 0x2c, 0x80, 0xf7, 0x74, 0xe7, 0xff, 0x21, 0x5a, 0x6a, 0x54, 0x1e, 0x41, 0x31, 0x92, 0x35, 0xc4, 0x33, 0x7, 0xa, 0xba, 0x7e, 0xe, 0x34, 0x88, 0xb1, 0x98, 0x7c, 0xf3, 0x3d, 0x60, 0x6c, 0x7b, 0xca, 0xd3, 0x1f, 0x32, 0x65, 0x4, 0x28, 0x64, 0xbe, 0x85, 0x9b, 0x2f, 0x59, 0x8a, 0xd7, 0xb0, 0x25, 0xac, 0xaf, 0x12, 0x3, 0xe2, 0xf2]
Zorro = [0xb2, 0xe5, 0x5e, 0xfd, 0x5f, 0xc5, 0x50, 0xbc, 0xdc, 0x4a, 0xfa, 0x88, 0x28, 0xd8, 0xe0, 0xd1, 0xb5, 0xd0, 0x3c, 0xb0, 0x99, 0xc1, 0xe8, 0xe2, 0x13, 0x59, 0xa7, 0xfb, 0x71, 0x34, 0x31, 0xf1, 0x9f, 0x3a, 0xce, 0x6e, 0xa8, 0xa4, 0xb4, 0x7e, 0x1f, 0xb7, 0x51, 0x1d, 0x38, 0x9d, 0x46, 0x69, 0x53, 0xe, 0x42, 0x1b, 0xf, 0x11, 0x68, 0xca, 0xaa, 0x6, 0xf0, 0xbd, 0x26, 0x6f, 0x0, 0xd9, 0x62, 0xf3, 0x15, 0x60, 0xf2, 0x3d, 0x7f, 0x35, 0x63, 0x2d, 0x67, 0x93, 0x1c, 0x91, 0xf9, 0x9c, 0x66, 0x2a, 0x81, 0x20, 0x95, 0xf8, 0xe3, 0x4d, 0x5a, 0x6d, 0x24, 0x7b, 0xb9, 0xef, 0xdf, 0xda, 0x58, 0xa9, 0x92, 0x76, 0x2e, 0xb3, 0x39, 0xc, 0x29, 0xcd, 0x43, 0xfe, 0xab, 0xf5, 0x94, 0x23, 0x16, 0x80, 0xc0, 0x12, 0x4c, 0xe9, 0x48, 0x19, 0x8, 0xae, 0x41, 0x70, 0x84, 0x14, 0xa2, 0xd5, 0xb8, 0x33, 0x65, 0xba, 0xed, 0x17, 0xcf, 0x96, 0x1e, 0x3b, 0xb, 0xc2, 0xc8, 0xb6, 0xbb, 0x8b, 0xa1, 0x54, 0x75, 0xc4, 0x10, 0x5d, 0xd6, 0x25, 0x97, 0xe6, 0xfc, 0x49, 0xf7, 0x52, 0x18, 0x86, 0x8d, 0xcb, 0xe1, 0xbf, 0xd7, 0x8e, 0x37, 0xbe, 0x82, 0xcc, 0x64, 0x90, 0x7c, 0x32, 0x8f, 0x4b, 0xac, 0x1a, 0xea, 0xd3, 0xf4, 0x6b, 0x2c, 0xff, 0x55, 0xa, 0x45, 0x9, 0x89, 0x1, 0x30, 0x2b, 0xd2, 0x77, 0x87, 0x72, 0xeb, 0x36, 0xde, 0x9e, 0x8c, 0xdb, 0x6c, 0x9b, 0x5, 0x2, 0x4e, 0xaf, 0x4, 0xad, 0x74, 0xc3, 0xee, 0xa6, 0xf6, 0xc7, 0x7d, 0x40, 0xd4, 0xd, 0x3e, 0x5b, 0xec, 0x78, 0xa0, 0xb1, 0x44, 0x73, 0x47, 0x5c, 0x98, 0x21, 0x22, 0x61, 0x3f, 0xc6, 0x7a, 0x56, 0xdd, 0xe7, 0x85, 0xc9, 0x8a, 0x57, 0x27, 0x7, 0x9a, 0x3, 0xa3, 0x83, 0xe4, 0x6a, 0xa5, 0x2f, 0x79, 0x4f]
iScream = [0x0, 0x85, 0x65, 0xd2, 0x5b, 0xff, 0x7a, 0xce, 0x4d, 0xe2, 0x2c, 0x36, 0x92, 0x15, 0xbd, 0xad, 0x57, 0xf3, 0x37, 0x2d, 0x88, 0xd, 0xac, 0xbc, 0x18, 0x9f, 0x7e, 0xca, 0x41, 0xee, 0x61, 0xd6, 0x59, 0xec, 0x78, 0xd4, 0x47, 0xf9, 0x26, 0xa3, 0x90, 0x8b, 0xbf, 0x30, 0xa, 0x13, 0x6f, 0xc0, 0x2b, 0xae, 0x91, 0x8a, 0xd8, 0x74, 0xb, 0x12, 0xcc, 0x63, 0xfd, 0x43, 0xb2, 0x3d, 0xe8, 0x5d, 0xb6, 0x1c, 0x83, 0x3b, 0xc8, 0x45, 0x9d, 0x24, 0x52, 0xdd, 0xe4, 0xf4, 0xab, 0x8, 0x77, 0x6d, 0xf5, 0xe5, 0x48, 0xc5, 0x6c, 0x76, 0xba, 0x10, 0x99, 0x20, 0xa7, 0x4, 0x87, 0x3f, 0xd0, 0x5f, 0xa5, 0x1e, 0x9b, 0x39, 0xb0, 0x2, 0xea, 0x67, 0xc6, 0xdf, 0x71, 0xf6, 0x54, 0x4f, 0x8d, 0x2e, 0xe7, 0x6a, 0xc7, 0xde, 0x35, 0x97, 0x55, 0x4e, 0x22, 0x81, 0x6, 0xb4, 0x7c, 0xfb, 0x1a, 0xa1, 0xd5, 0x79, 0xfc, 0x42, 0x84, 0x1, 0xe9, 0x5c, 0x14, 0x93, 0x33, 0x29, 0xc1, 0x6e, 0xa8, 0xb8, 0x28, 0x32, 0xc, 0x89, 0xb9, 0xa9, 0xd9, 0x75, 0xed, 0x58, 0xcd, 0x62, 0xf8, 0x46, 0x9e, 0x19, 0xcb, 0x7f, 0xa2, 0x27, 0xd7, 0x60, 0xfe, 0x5a, 0x8e, 0x95, 0xe3, 0x4c, 0x16, 0xf, 0x31, 0xbe, 0x64, 0xd3, 0x3c, 0xb3, 0x7b, 0xcf, 0x40, 0xef, 0x8f, 0x94, 0x56, 0xf2, 0x17, 0xe, 0xaf, 0x2a, 0x2f, 0x8c, 0xf1, 0xe1, 0xdc, 0x53, 0x68, 0x72, 0x44, 0xc9, 0x1b, 0xa0, 0x38, 0x9a, 0x7, 0xb5, 0x5e, 0xd1, 0x3, 0xb1, 0x23, 0x80, 0x1f, 0xa4, 0x34, 0x96, 0xe0, 0xf0, 0xc4, 0x49, 0x73, 0x69, 0xda, 0xc3, 0x9, 0xaa, 0x4a, 0x51, 0xf7, 0x70, 0x3e, 0x86, 0x66, 0xeb, 0x21, 0x98, 0x1d, 0xb7, 0xdb, 0xc2, 0xbb, 0x11, 0x4b, 0x50, 0x6b, 0xe6, 0x9c, 0x25, 0xfa, 0x7d, 0x82, 0x3a, 0xa6, 0x5]
keccak_chi_5 = [0x0, 0x5, 0xa, 0xb, 0x14, 0x11, 0x16, 0x17, 0x9, 0xc, 0x3, 0x2, 0xd, 0x8, 0xf, 0xe, 0x12, 0x15, 0x18, 0x1b, 0x6, 0x1, 0x4, 0x7, 0x1a, 0x1d, 0x10, 0x13, 0x1e, 0x19, 0x1c, 0x1f]
misty_s7 = [0x36, 0x32, 0x3e, 0x38, 0x16, 0x22, 0x5e, 0x60, 0x26, 0x6, 0x3f, 0x5d, 0x2, 0x12, 0x7b, 0x21, 0x37, 0x71, 0x27, 0x72, 0x15, 0x43, 0x41, 0xc, 0x2f, 0x49, 0x2e, 0x1b, 0x19, 0x6f, 0x7c, 0x51, 0x35, 0x9, 0x79, 0x4f, 0x34, 0x3c, 0x3a, 0x30, 0x65, 0x7f, 0x28, 0x78, 0x68, 0x46, 0x47, 0x2b, 0x14, 0x7a, 0x48, 0x3d, 0x17, 0x6d, 0xd, 0x64, 0x4d, 0x1, 0x10, 0x7, 0x52, 0xa, 0x69, 0x62, 0x75, 0x74, 0x4c, 0xb, 0x59, 0x6a, 0x0, 0x7d, 0x76, 0x63, 0x56, 0x45, 0x1e, 0x39, 0x7e, 0x57, 0x70, 0x33, 0x11, 0x5, 0x5f, 0xe, 0x5a, 0x54, 0x5b, 0x8, 0x23, 0x67, 0x20, 0x61, 0x1c, 0x42, 0x66, 0x1f, 0x1a, 0x2d, 0x4b, 0x4, 0x55, 0x5c, 0x25, 0x4a, 0x50, 0x31, 0x44, 0x1d, 0x73, 0x2c, 0x40, 0x6b, 0x6c, 0x18, 0x6e, 0x53, 0x24, 0x4e, 0x2a, 0x13, 0xf, 0x29, 0x58, 0x77, 0x3b, 0x3]
misty_s9 = [0xa7, 0xef, 0xa1, 0x17b, 0x187, 0x14e, 0x9, 0x152, 0x26, 0xe2, 0x30, 0x166, 0x1c4, 0x181, 0x5a, 0x18d, 0xb7, 0xfd, 0x93, 0x14b, 0x19f, 0x154, 0x33, 0x16a, 0x132, 0x1f4, 0x106, 0x52, 0xd8, 0x9f, 0x164, 0xb1, 0xaf, 0xf1, 0x1e9, 0x25, 0xce, 0x11, 0x0, 0x14d, 0x2c, 0xfe, 0x17a, 0x3a, 0x8f, 0xdc, 0x51, 0x190, 0x5f, 0x3, 0x13b, 0xf5, 0x36, 0xeb, 0xda, 0x195, 0x1d8, 0x108, 0xac, 0x1ee, 0x173, 0x122, 0x18f, 0x4c, 0xa5, 0xc5, 0x18b, 0x79, 0x101, 0x1e0, 0x1a7, 0xd4, 0xf0, 0x1c, 0x1ce, 0xb0, 0x196, 0x1fb, 0x120, 0xdf, 0x1f5, 0x197, 0xf9, 0x109, 0x59, 0xba, 0xdd, 0x1ac, 0xa4, 0x4a, 0x1b8, 0xc4, 0x1ca, 0x1a5, 0x15e, 0xa3, 0xe8, 0x9e, 0x86, 0x162, 0xd, 0xfa, 0x1eb, 0x8e, 0xbf, 0x45, 0xc1, 0x1a9, 0x98, 0xe3, 0x16e, 0x87, 0x158, 0x12c, 0x114, 0xf2, 0x1b5, 0x140, 0x71, 0x116, 0xb, 0xf3, 0x57, 0x13d, 0x24, 0x5d, 0x1f0, 0x1b, 0x1e7, 0x1be, 0x1e2, 0x29, 0x44, 0x9c, 0x1c9, 0x83, 0x146, 0x193, 0x153, 0x14, 0x27, 0x73, 0x1ba, 0x7c, 0x1db, 0x180, 0x1fc, 0x35, 0x70, 0xaa, 0x1df, 0x97, 0x7e, 0xa9, 0x49, 0x10c, 0x117, 0x141, 0xa8, 0x16c, 0x16b, 0x124, 0x2e, 0x1f3, 0x189, 0x147, 0x144, 0x18, 0x1c8, 0x10b, 0x9d, 0x1cc, 0x1e8, 0x1aa, 0x135, 0xe5, 0x1b7, 0x1fa, 0xd0, 0x10f, 0x15d, 0x191, 0x1b2, 0xec, 0x10, 0xd1, 0x167, 0x34, 0x38, 0x78, 0xc7, 0x115, 0x1d1, 0x1a0, 0xfc, 0x11f, 0xf6, 0x6, 0x53, 0x131, 0x1a4, 0x159, 0x99, 0x1f6, 0x41, 0x3d, 0xf4, 0x11a, 0xad, 0xde, 0x1a2, 0x43, 0x182, 0x170, 0x105, 0x65, 0x1dc, 0x123, 0xc3, 0x1ae, 0x31, 0x4f, 0xa6, 0x14a, 0x118, 0x17f, 0x175, 0x80, 0x17e, 0x198, 0x9b, 0x1ef, 0x16f, 0x184, 0x112, 0x6b, 0x1cb, 0x1a1, 0x3e, 0x1c6, 0x84, 0xe1, 0xcb, 0x13c, 0xea, 0xe, 0x12d, 0x5b, 0x1f7, 0x11e, 0x1a8, 0xd3, 0x15b, 0x133, 0x8c, 0x176, 0x23, 0x67, 0x7d, 0x1ab, 0x13, 0xd6, 0x1c5, 0x92, 0x1f2, 0x13a, 0x1bc, 0xe6, 0x100, 0x149, 0xc6, 0x11d, 0x32, 0x74, 0x4e, 0x19a, 0xa, 0xcd, 0x1fe, 0xab, 0xe7, 0x2d, 0x8b, 0x1d3, 0x1d, 0x56, 0x1f9, 0x20, 0x48, 0x1a, 0x156, 0x96, 0x139, 0x1ea, 0x1af, 0xee, 0x19b, 0x145, 0x95, 0x1d9, 0x28, 0x77, 0xae, 0x163, 0xb9, 0xe9, 0x185, 0x47, 0x1c0, 0x111, 0x174, 0x37, 0x6e, 0xb2, 0x142, 0xc, 0x1d5, 0x188, 0x171, 0xbe, 0x1, 0x6d, 0x177, 0x89, 0xb5, 0x58, 0x4b, 0x134, 0x104, 0x1e4, 0x62, 0x110, 0x172, 0x113, 0x19c, 0x6f, 0x150, 0x13e, 0x4, 0x1f8, 0x1ec, 0x103, 0x130, 0x4d, 0x151, 0x1b3, 0x15, 0x165, 0x12f, 0x14c, 0x1e3, 0x12, 0x2f, 0x55, 0x19, 0x1f1, 0x1da, 0x121, 0x64, 0x10d, 0x128, 0x1de, 0x10e, 0x6a, 0x1f, 0x68, 0x1b1, 0x54, 0x19e, 0x1e6, 0x18a, 0x60, 0x63, 0x9a, 0x1ff, 0x94, 0x19d, 0x169, 0x199, 0xff, 0xa2, 0xd7, 0x12e, 0xc9, 0x10a, 0x15f, 0x157, 0x90, 0x1b9, 0x16d, 0x6c, 0x12a, 0xfb, 0x22, 0xb6, 0x1fd, 0x8a, 0xd2, 0x14f, 0x85, 0x137, 0x160, 0x148, 0x8d, 0x18c, 0x15a, 0x7b, 0x13f, 0x1c2, 0x119, 0x1ad, 0xe4, 0x1bb, 0x1e1, 0x5c, 0x194, 0x1e5, 0x1a6, 0xf8, 0x129, 0x17, 0xd5, 0x82, 0x1d2, 0x16, 0xd9, 0x11b, 0x46, 0x126, 0x168, 0x1a3, 0x7f, 0x138, 0x179, 0x7, 0x1d4, 0xc2, 0x2, 0x75, 0x127, 0x1cf, 0x102, 0xe0, 0x1bf, 0xf7, 0xbb, 0x50, 0x18e, 0x11c, 0x161, 0x69, 0x186, 0x12b, 0x1d7, 0x1d6, 0xb8, 0x39, 0xc8, 0x15c, 0x3f, 0xcc, 0xbc, 0x21, 0x1c3, 0x61, 0x1e, 0x136, 0xdb, 0x5e, 0xa0, 0x81, 0x1ed, 0x40, 0xb3, 0x107, 0x66, 0xbd, 0xcf, 0x72, 0x192, 0x1b6, 0x1dd, 0x183, 0x7a, 0xc0, 0x2a, 0x17d, 0x5, 0x91, 0x76, 0xb4, 0x1c1, 0x125, 0x143, 0x88, 0x17c, 0x2b, 0x42, 0x3c, 0x1c7, 0x155, 0x1bd, 0xca, 0x1b0, 0x8, 0xed, 0xf, 0x178, 0x1b4, 0x1d0, 0x3b, 0x1cd]


if 0:  # code for generating Keccak S-box
    keccak_chi_5 = []
    from binteger import Bin
    for x in range(32):
        x = Bin(x, 5).tuple
        y = [x[i] ^ (1^x[(i+1)%5])&x[(i+2)%5] for i in range(5)]
        keccak_chi_5.append(Bin(y).int)
    del x, y


def make_sbox(sbox):
    n = len(sbox).bit_length() - 1
    assert len(sbox) == 2**n
    assert 0 == min(sbox) < max(sbox) == 2**n-1
    return Sbox(sbox, n, n)


# Dictionary of all available SBoxes
sboxes = {}
for k, v in list(globals().items()):
    if isinstance(v, list):
        sboxes[k] = make_sbox(tuple(v))
        if __name__ == '__main__':
            print(f"{k} = [" + ", ".join("0x%x" % y for y in v) + "]")