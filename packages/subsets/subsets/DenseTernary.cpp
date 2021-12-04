#include <DenseTernary.hpp>


DenseTernary::DenseTernary() {
    n = 0;
    fullsize = 1;
    data.resize(1);
}
DenseTernary::DenseTernary(int _n) {
    n = _n;
    fullsize = pow3(n);
    size_t n_bitsets = (fullsize + BITSET3_PER3 - 1) / BITSET3_PER3;
    data.resize(n_bitsets);
}
DenseTernary::DenseTernary(const DenseSet & d) {
    n = d.n;
    fullsize = pow3(n);
    size_t n_bitsets = (fullsize + BITSET3_PER3 - 1) / BITSET3_PER3;
    data.resize(n_bitsets);

    auto func = [&] (uint64_t x) -> void {
        set(bin2ter(x, d.n));
    };
    d.iter_support(func);
}

int DenseTernary::get(uint64_t x) const {
    ensure(0 <= x && x < fullsize);
    return data[HI(x)][LO(x)];
}
void DenseTernary::set(uint64_t x) {
    ensure(0 <= x && x < fullsize);
    data[HI(x)][LO(x)] = 1;
}

void DenseTernary::iter_support(std::function<void(uint64_t x)> const & func) const {
    fori(hi, data.size()) {
        if (data[hi].any()) {
            auto &w = data[hi];
            auto hi3 = hi * BITSET3_PER3;
            fori(lo, BITSET3_PER3) {
                if (w[lo]) {
                    func(hi3 + lo);
                }
            }
        }
    }
}

std::vector<uint64_t> DenseTernary::get_support() const {
    vector<uint64_t> inds;
    auto func = [&] (uint64_t v) -> void { inds.push_back(v); };
    iter_support(func);
    return inds;
}
uint64_t DenseTernary::get_weight() const {
    uint64_t ret = 0;
    fori(hi, data.size()) {
        if (data[hi].any()) {
            ret += data[hi].count();
        }
    }
    return ret;
}

void DenseTernary::do_Sweep_QmC_AND_up_OR(uint64_t mask) {
    do_Sweep<QmC_AND_up_OR<BITSET3>>(mask);
}
void DenseTernary::do_Sweep_QmC_NOTAND_down(uint64_t mask) {
    do_Sweep<QmC_NOTAND_down<BITSET3>>(mask);
}
void DenseTernary::do_QuineMcCluskey(uint64_t mask) {
    do_Sweep_QmC_AND_up_OR(mask);
    do_Sweep_QmC_NOTAND_down(mask);
}