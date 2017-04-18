//
//  indexFunc.cpp
//  
//
//
//
//

#include "header.hpp"

/************************************************************
 Index Linearizing function
 ************************************************************/

dictionary sub2ind(const dictionary i, const dictionary j, const dictionary ncol) {
    return (i*ncol + j);
}

/************************************************************
 1D index -> 2D index function
 ************************************************************/

dictionary ind2sub_i(const dictionary idx, const dictionary ncol){
    return (int)(idx / ncol) ;
}
dictionary ind2sub_j(const dictionary idx, const dictionary ncol){
    return idx % ncol;
}


/************************************************************
 Convert string tokens to numeric indices using Dictionary index
 ************************************************************/

void lookup_word_dictionary(const vec_str token, vec_idx& word, const hashtable wordList_by_word){
    
    int n = (int)token.size();
    dictionary num_word_univ = wordList_by_word.size();
    
    hashtable::const_iterator got;
    dictionary temp_word_idx;
    
    /* Assign number for each word */
    for(int i=0; i<n ; i++){
        
        got = wordList_by_word.find(token[i]);
        // If can't find the word, assign it to be "__ENTITY"
        
        if (got == wordList_by_word.end())
            temp_word_idx = num_word_univ - 1;
        else
            temp_word_idx = got->second;
        
        word[i] = temp_word_idx;
    }
}
