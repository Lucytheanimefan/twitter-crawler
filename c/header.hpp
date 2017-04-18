//
//  header.hpp
//  
//
//
//
//

#ifndef header

#define header

#include <Python.h>      // Python implementation
#include <assert.h>     // assert
#include <vector>       // vector
#include <limits>       // inf
#include <fstream>      // std::ifstream
#include <iostream>     // cout, endl
#include <stdlib.h>     // Python implementation
#include <unordered_map>    // hashtable implementation

#define pos_inf std::numeric_limits<real>::infinity();
#define neg_inf (-1)*std::numeric_limits<real>::infinity();

/* aliasing */
using dictionary = unsigned long long int;
using real = double;
using string = std::string;
using vec_idx = std::vector<dictionary>;
using vec = std::vector<real>;
using vec_str = std::vector<string>;

using hashtable = std::unordered_map<string,dictionary>;
using pair = std::pair<string, dictionary>;

/* Indexing function */
dictionary sub2ind(const dictionary, const dictionary, const dictionary);
dictionary ind2sub_i(const dictionary, const dictionary);
dictionary ind2sub_j(const dictionary, const dictionary);

void lookup_word_dictionary(const vec_str token, vec_idx& word, const hashtable wordList_by_word);

/* Loading Tag & Word Dictionary function */
void load_dictionary(hashtable& List_by_str, vec_str& List_by_idx, const string filename);

/* Loading & Saving parameters function */
void load_param(vec& prob, const dictionary num_row, const dictionary num_col, const string filename);
//void save_param(vec prob, dictionary num_row, dictionary num_col, string filename);

/* Viterbi Algorithm */
void viterbi(const vec_idx word, vec_idx& tag,
             const vec prob_tag, const vec prob_word_given_tag, const vec prob_transition,
             dictionary num_tag_univ);

void maximizePath(vec& delta_val, vec_idx& delta_maxIdx, const vec_idx word,
                         const int num_token, const dictionary num_tag_univ,
                         const vec prob_transition, const vec prob_tag, const vec prob_word_given_tag);

void recoverPath(const vec delta_val, const vec_idx delta_maxIdx, vec_idx& tag_path,
                 const dictionary num_token, const dictionary num_tag_univ);

void delta_0_update(vec& delta_val, const dictionary word_idx, const dictionary num_tag_univ,
                           const vec prob_tag, const vec prob_word_given_tag);
void delta_n_update(vec& delta_val, vec_idx& delta_maxIdx, const dictionary idx,
                    const dictionary word_idx, const dictionary num_tag_univ,
                    const vec prob_transition, const vec prob_word_given_tag);

void maximum(const vec delta_val, const dictionary idx, real& max_val,
                    dictionary& max_idx, const dictionary num_tag_univ);


#endif /* header_hpp */
