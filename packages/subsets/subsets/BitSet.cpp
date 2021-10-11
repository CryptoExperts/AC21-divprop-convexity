#include <sstream>

#include "common.hpp"

#include "BitSet.hpp"

using namespace Pack64;

bool BitSet::QUIET = false;

void BitSet::set_quiet(bool value) {
    BitSet::QUIET = value;
}

BitSet::BitSet(const vector<uint64_t> &_data) {
    n = _data.size() << 6;
    data = _data;
    _trim();
}
BitSet::BitSet(const string &_bits) {
    n = _bits.size();
    data.resize( HI(n) + (LO(n) != 0) );
    fori (i, (uint64_t)_bits.size()) {
        ensure(_bits[i] == 0x30 || _bits[i] == 0x31);
        data[HI(i)] |= (_bits[i] - 0x30ull) << LO(i);
    }
}
BitSet::BitSet(const vector<char> &_bits) {
    n = _bits.size();
    data.resize( HI(n) + (LO(n) != 0) );
    fori (i, (uint64_t)_bits.size()) {
        data[HI(i)] |= (_bits[i] & 1ull) << LO(i);
    }
}
BitSet BitSet::copy() const {
    return *this;
}
void BitSet::resize(uint64_t n) {
    // WARNING: keeps only "small" values if n decreases
    this->n = n;
    data.resize(HICEIL(n));
    _trim();
}

uint64_t BitSet::nwords() const {
    return HICEIL(n);
}

void BitSet::_trim() {
    if (LO(n)) {
        data.back() &= (1ull << LO(n)) - 1;
    }
}


int BitSet::get(uint64_t x) const {
    ensure(x < n);
    return (data[HI(x)] >> LO(x)) & 1;
}
void BitSet::set(uint64_t x) {
    ensure(x < n);
    data[HI(x)] |= 1ull << LO(x);
}
void BitSet::unset(uint64_t x) {
    ensure(x < n);
    data[HI(x)] &= ~(1ull << LO(x));
}
void BitSet::set(uint64_t x, uint64_t value) {
    ensure(x < n);
    data[HI(x)] &= ~(1ull << LO(x));
    data[HI(x)] |= (value & 1ull) << LO(x);
}
void BitSet::add(uint64_t x) {
    set(x);
}
void BitSet::remove(uint64_t x) {
    ensure(get(x));
    unset(x);
}
void BitSet::discard(uint64_t x) {
    unset(x);
}

void BitSet::clear() {
    n = 0;
    data.clear();
}
void BitSet::empty() {
    if (n == 0) {
        data.clear();
        return;
    }
    data.assign(nwords(), 0);
}
void BitSet::fill() {
    if (n == 0) {
        return;
    }
    data.assign(nwords(), -1ull);
    _trim();
}


bool BitSet::is_empty() const {
    for(uint64_t v: data) {
        if (v) {
            return false;
        }
    }
    return true;
}
bool BitSet::is_full() const {
    fori(i, nwords() - 1) {
        if (data[i] != -1ull) {
            return false;
        }
    }
    if (LO(n)) {
        return data.back() == (1ull << LO(n)) - 1;
    }
    else {
        return data.back() == -1ull;
    }
}


void BitSet::iter_support(function<void(uint64_t)> const & func) const {
    fori(hi, nwords() - 1) {
        if (data[hi]) {
            fori(lo, 64) {
                if ((data[hi] >> lo) & 1) {
                    func((hi << 6) | lo);
                }
            }
        }
    }
    uint64_t hi = nwords() - 1;
    uint64_t remaining = LO(n) ? LO(n) : 64;
    fori(lo, remaining) {
        if ((data[hi] >> lo) & 1) {
            func((hi << 6) | lo);
        }
    }
}
uint64_t BitSet::get_weight() const {
    uint64_t cnt = 0;
    for(uint64_t v: data) {
        if (v) {
            cnt += hw(v);
        }
    }
    return cnt;
}
vector<uint64_t> BitSet::get_support() const {
    vector<uint64_t> inds;
    auto func = [&] (uint64_t v) -> void { inds.push_back(v); };
    iter_support(func);
    return inds;
}


string BitSet::str() const {
    stringstream ss;
    fori (i, (uint64_t)n) {
        ss << get(i);
    }
    return ss.str();
}
string BitSet::info() const {
    char buf[4096] = {};
    snprintf(
        buf, 4000,
        "<BitSet hash=%016lx n=%lu wt=%lu>",
        get_hash(), n, get_weight()
    );
    return string(buf);
}
uint64_t BitSet::get_hash() const {
    uint64_t h = -1ull;
    for (auto v: data) {
        h ^= v;
        h *= 0xcaffee1234abcdefull;
        h ^= h >> 12;
        h += v;
        h ^= h >> 17;
    }
    return h;
}


BitSet& BitSet::operator|=(const BitSet &bs) {
    ensure(n == bs.n);
    auto &data2 = bs.data;
    fori (i, nwords()) {
        data[i] |= data2[i];
    }
    return *this;
}
BitSet& BitSet::operator^=(const BitSet &bs) {
    ensure(n == bs.n);
    auto &data2 = bs.data;
    fori (i, nwords()) {
        data[i] ^= data2[i];
    }
    return *this;
}
BitSet& BitSet::operator&=(const BitSet &bs) {
    ensure(n == bs.n);
    auto &data2 = bs.data;
    fori (i, nwords()) {
        data[i] &= data2[i];
    }
    return *this;
}
BitSet& BitSet::operator-=(const BitSet &bs) {
    ensure(n == bs.n);
    auto &data2 = bs.data;
    fori(i, nwords()) {
        data[i] &= ~data2[i];
    }
    return *this;
}
BitSet BitSet::operator^(const BitSet &bs) const {
    ensure(n == bs.n);
    BitSet res = *this;
    res ^= bs;
    return res;
}
BitSet BitSet::operator|(const BitSet &bs) const {
    ensure(n == bs.n);
    BitSet res = *this;
    res |= bs;
    return res;
}
BitSet BitSet::operator&(const BitSet &bs) const {
    ensure(n == bs.n);
    BitSet res = *this;
    res &= bs;
    return res;
}
BitSet BitSet::operator-(const BitSet &bs) const {
    ensure(n == bs.n);
    BitSet res = *this;
    res -= bs;
    return res;
}
// BitSet BitSet::operator~() const {
//     return Complement();
// }



bool BitSet::operator==(const BitSet & bs) const {
    ensure(n == bs.n, "bitsets must have same dimension");
    return data == bs.data;
}
bool BitSet::operator!=(const BitSet & bs) const {
    ensure(n == bs.n, "bitsets must have same dimension");
    return data != bs.data;
}
bool BitSet::operator<(const BitSet & bs) const {
    ensure(n == bs.n, "bitsets must have same dimension");
    auto &data2 = bs.data;
    bool not_equal = false;
    fori(i, data.size()) {
        if (data[i] == data2[i]) continue;
        not_equal = true;
        // (not <=) means (not <)
        if ((data[i] & data2[i]) != data[i])  return false;
    }
    return not_equal;
}
bool BitSet::operator>(const BitSet & bs) const {
    ensure(n == bs.n, "bitsets must have same dimension");
    auto &data2 = bs.data;
    bool not_equal = false;
    fori(i, data.size()) {
        if (data[i] == data2[i]) continue;
        not_equal = true;
        // (not >=) means (not >)
        if ((data[i] & data2[i]) != data2[i])  return false;
    }
    return not_equal;
}
bool BitSet::operator<=(const BitSet & bs) const {
    ensure(n == bs.n, "bitsets must have same dimension");
    auto &data2 = bs.data;
    fori(i, data.size()) {
        if (data[i] == data2[i]) continue;
        // (not <=) means (not <)
        if ((data[i] & data2[i]) != data[i])  return false;
    }
    return true;
}
bool BitSet::operator>=(const BitSet & bs) const {
    ensure(n == bs.n, "bitsets must have same dimension");
    auto &data2 = bs.data;
    fori(i, data.size()) {
        if (data[i] == data2[i]) continue;
        // (not >=) means (not >)
        if ((data[i] & data2[i]) != data2[i])  return false;
    }
    return true;
}

void BitSet::do_Complement() {
    fori(i, nwords()) {
        data[i] = ~data[i];
    }
    _trim();
}

BitSet BitSet::Complement() const {
    auto ret = copy();
    ret.do_Complement();
    return ret;
}


// ========================================
// Stuff
// ========================================
void BitSet::save_to_file(const char *filename) const {
    if (!QUIET) {
        fprintf(stderr, "Saving BitSet(n=%lu) to %s\n", n, filename);
    }

    FILE *fd = fopen(filename, "w");
    ensure(fd, "can not open file");

    save_to_file(fd);

    fclose(fd);
}
BitSet BitSet::load_from_file(const char *filename) {
    FILE *fd = fopen(filename, "r");
    ensure(fd, "can not open file");

    auto ret = load_from_file(fd);

    fclose(fd);
    return ret;
}
void BitSet::save_to_file(FILE *fd) const {
    uint64_t vn = n;
    uint64_t sz = 8;
    if (n < 1ull << 8) {
        sz = 1;
    }
    else if (n < 1ull << 16) {
        sz = 2;
    }
    else if (n < 1ull << 32) {
        sz = 4;
    }

    vector<uint64_t> supp = get_support();
    if (supp.size() * sz < data.size() * 8) {
        uint64_t header = BitSet::VERSION_SPARSE;
        uint64_t vl = supp.size();

        ensure(1 == fwrite(&header, 8, 1, fd));
        ensure(1 == fwrite(&vn, 8, 1, fd));
        ensure(1 == fwrite(&vl, 8, 1, fd));
        ensure(1 == fwrite(&sz, 8, 1, fd));

        if (sz == 1) {
            vector<uint8_t> supp_supp(supp.begin(), supp.end());
            ensure(supp.size() == fwrite(supp_supp.data(), sz, supp.size(), fd));
        }
        else if (sz == 2) {
            vector<uint16_t> supp_supp(supp.begin(), supp.end());
            ensure(supp.size() == fwrite(supp_supp.data(), sz, supp.size(), fd));
        }
        else if (sz == 4) {
            vector<uint32_t> supp_supp(supp.begin(), supp.end());
            ensure(supp.size() == fwrite(supp_supp.data(), sz, supp.size(), fd));
        }
        else if (sz == 8) {
            ensure(supp.size() == fwrite(supp.data(), sz, supp.size(), fd));
        }
        else {
            ensure(0, "???");
        }

        uint64_t marker = MARKER_END;
        ensure(1 == fwrite(&marker, 8, 1, fd));
    }
    else {
        supp.clear();

        uint64_t header = BitSet::VERSION_DENSE;
        uint64_t vl = data.size();

        ensure(1 == fwrite(&header, 8, 1, fd));
        ensure(1 == fwrite(&vn, 8, 1, fd));
        ensure(1 == fwrite(&vl, 8, 1, fd));
        ensure(1 == fwrite(&sz, 8, 1, fd));

        ensure(vl == fwrite(data.data(), sizeof(uint64_t), vl, fd));

        uint64_t marker = MARKER_END;
        ensure(1 == fwrite(&marker, 8, 1, fd));
    }
}
BitSet BitSet::load_from_file(FILE *fd) {

    BitSet res;

    uint64_t header;
    ensure(1 == fread(&header, 8, 1, fd));

    uint64_t vn;
    uint64_t vl;
    uint64_t sz;
    ensure(1 == fread(&vn, 8, 1, fd));
    ensure(1 == fread(&vl, 8, 1, fd));
    ensure(1 == fread(&sz, 8, 1, fd));

    if (header == VERSION_SPARSE) {
        if (!QUIET) {
            fprintf(stderr,
                "Loading BitSet(n=%lu)"
                " with weight %lu"
                " (%lu bytes per elem.)\n",
                vn, vl, sz
            );
        }

        res = BitSet(vn);
        if (sz == 1) {
            vector<uint8_t> supp(vl);
            ensure(vl == fread(supp.data(), sz, vl, fd));
            for (auto v: supp) res.add(v);
        }
        else if (sz == 2) {
            vector<uint16_t> supp(vl);
            ensure(vl == fread(supp.data(), sz, vl, fd));
            for (auto v: supp) res.add(v);
        }
        else if (sz == 4) {
            vector<uint32_t> supp(vl);
            ensure(vl == fread(supp.data(), sz, vl, fd));
            for (auto v: supp) res.add(v);
        }
        else if (sz == 8) {
            vector<uint64_t> supp(vl);
            ensure(vl == fread(supp.data(), sz, vl, fd));
            for (auto v: supp) res.add(v);
        }
        else {
            ensure(0, "???");
        }
    }
    else if (header == VERSION_DENSE) {
        if (!QUIET) {
            fprintf(stderr,
                "Loading BitSet(n=%lu)"
                " with %lu words"
                " (%lu bytes per elem.)\n",
                vn, vl, sz
            );
        }
        res = BitSet(vn);
        ensure(sizeof(res.data[0]) == 8);
        ensure(res.data.size() == vl);
        ensure(vl == fread(res.data.data(), 8, vl, fd));
    }
    else {
        ensure(0, "unknown set file version");
    }
    uint64_t marker;
    ensure(1 == fread(&marker, 8, 1, fd));
    ensure(marker == MARKER_END, "file format error");

    return res;
}

uint64_t BitSet::_get_data_ptr() const {
    return (uint64_t)data.data();
}