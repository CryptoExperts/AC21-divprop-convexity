%module(package="subsets") subsets

%include <std_vector.i>
%include <std_string.i>
%include <exception.i>
%include <std_map.i>
%include <std_set.i>
%include <stdint.i>

%template(MyVectorVector_u64) std::vector<std::vector<uint64_t>>;
%template(MyVector_u64) std::vector<uint64_t>;
%template(MyVector_i64) std::vector<int64_t>;
// %template(MyVector_u32) std::vector<uint32_t>;
// %template(MyVector_u16) std::vector<uint16_t>;
// %template(MyVector_u8) std::vector<uint8_t>;
%template(MyVector_int) std::vector<int>;
%template(MySet_uint64) std::set<uint64_t>;
%template(MyMap_PII_u64) std::map<std::pair<int,int>, uint64_t>;

// https://stackoverflow.com/questions/1394484/how-do-i-propagate-c-exceptions-to-python-in-a-swig-wrapper-library
// TBD: maybe translate some C++ exceptions into Python analogues
%exception {
    try {
        $action
    } catch(const std::exception& e) {
        SWIG_exception(SWIG_RuntimeError, e.what());
    } catch (...) {
        SWIG_exception(SWIG_UnknownError, "unknown exception");
    }
}

%{
#include "BitSet.hpp"
#include "DenseSet.hpp"
#include "DenseBox.hpp"
#include "DenseTernary.hpp"
%}

%include "BitSet.hpp"
%include "DenseSet.hpp"
%include "DenseBox.hpp"
%include "DenseTernary.hpp"

%template(Vec_DenseSet) std::vector<DenseSet>;
%template(Vec_DenseBox) std::vector<DenseBox>;
%template(Vec_DenseTernary) std::vector<DenseTernary>;