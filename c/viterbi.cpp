//
//  viterbi.cpp
//  
//
//
//
//

/* Reference :
 1. Hidden Markov Model : http://www.cs.ubc.ca/~murphyk/Bayes/rabiner.pdf
 2. Active Learning : http://www.machinelearning.org/proceedings/icml2005/papers/002_Active_AndersonMoore.pdf
 */

#include "header.hpp"

/* forward function declarations */
inline void delta_0_update(vec& delta_val, const dictionary word_idx, const dictionary num_tag_univ,
                           const vec prob_tag, const vec prob_word_given_tag);
inline void delta_n_update(vec& delta_val, vec_idx& delta_maxIdx, const dictionary idx,
                           const dictionary word_idx, const dictionary num_tag_univ,
                           const vec prob_transition, const vec prob_word_given_tag);


///**********************************<Main Algorithms>**********************************/
//
///************************************************************
// Part of Speech(POS) Bigram tagging
// ************************************************************/
//
//double pos_tag(tweet){
//
//    /* tokenize the given tweet */
//    vec_idx word;
//    tokenize(tweet, word);
//
//    /* number of tokens for the given tweet */
//    size_t num_token = word.size();
//
//    /* tag associated with each tokenized word */
//    vec_idx tag;
//    tag.resize(num_token);
//
//    /* viterbi algorithm to find the maximizing path (=sequence of tags) */
//    viterbi(word, tag, num_token);
//
//}
//


/************************************************************
 Viterbi path algorithm (dynamic programming), bigram tagging
 ************************************************************/

/***** word and tag are arrays of indicies *****/
void viterbi(const vec_idx word, vec_idx& tag,
             const vec prob_tag, const vec prob_word_given_tag, const vec prob_transition,
             dictionary num_tag_univ){
    
    const int num_token = (int)word.size();
    
    /******************
     Temporary variables
     ******************/
    /* delta function table, delta(idx,tag), idx :row, tag:column*/
    vec delta_val;  /* delta function matrix, 0-initialized */
    vec_idx delta_maxIdx;  /* maximizing index (of previous node) matrix, 0-initialized */
    delta_val.resize(num_token * num_tag_univ);
    delta_maxIdx.resize(num_token * num_tag_univ);
    
    
    /******************
     Main algorithm
     ******************/
    maximizePath(delta_val, delta_maxIdx, word, num_token, num_tag_univ,
                 prob_transition, prob_tag, prob_word_given_tag);
    recoverPath(delta_val, delta_maxIdx, tag, num_token, num_tag_univ);
    
}

/************************************************************
 Viterbi forward calculation
 ************************************************************/

void maximizePath(vec& delta_val, vec_idx& delta_maxIdx, const vec_idx word,
                  const int num_token, const dictionary num_tag_univ,
                  const vec prob_transition, const vec prob_tag, const vec prob_word_given_tag){
    
    for(int i=0; i<num_token ; i++){
        
        if (i==0)
            delta_0_update(delta_val, word[0],
                           num_tag_univ, prob_tag, prob_word_given_tag);
        else
            delta_n_update(delta_val, delta_maxIdx, i, word[i],
                           num_tag_univ, prob_transition, prob_word_given_tag);
        
    }
}

/************************************************************
 Viterbi backtracking (recovering path sequence)
 ************************************************************/

/* find tag path(=sequence of tag states) maximizing the likelihood */

void recoverPath(const vec delta_val, const vec_idx delta_maxIdx, vec_idx& tag_path,
                 const dictionary num_token, const dictionary num_tag_univ){
    
    real max_val;
    dictionary max_idx;
    
    for (int i = num_token-1 ; i>=0 ; i--){
        
        max_val = neg_inf;
        max_idx = 0;
        
        if (i == (num_token - 1)){
            maximum(delta_val, i, max_val, max_idx, num_tag_univ);
            tag_path[i] = max_idx;
        }
        else{
            tag_path[i] = delta_maxIdx[sub2ind(i, tag_path[i+1], num_tag_univ)];
            
        }
    }
    
}



/**********************************<Function related to Delta>**********************************/

/************************************************************
 Delta Update functions
 ************************************************************/

/* for the first word in a sentence */
void delta_0_update(vec& delta_val, const dictionary word_idx, const dictionary num_tag_univ,
                    const vec prob_tag, const vec prob_word_given_tag){
    
    for(dictionary tag=0; tag<num_tag_univ ; tag++){
        delta_val[sub2ind(0,tag,num_tag_univ)] =
        prob_tag[tag] * prob_word_given_tag[sub2ind(word_idx, tag, num_tag_univ)];
    }
    
}

/* for the rest of the words in a sentence */
void delta_n_update(vec& delta_val, vec_idx& delta_maxIdx, const dictionary idx,
                    const dictionary word_idx, const dictionary num_tag_univ,
                    const vec prob_transition, const vec prob_word_given_tag){
    
    real max_val;
    dictionary max_idx;
    
    real temp;
    
    /*** this for loop can be parallelized using cilk ***/
    for(int tag_curr=0; tag_curr<num_tag_univ ; tag_curr++){
        
        max_val = neg_inf;
        max_idx = 0;
        temp = 0;
        
        /*** this for loop cannot be parallelized ***/
        for(int tag_prev=0; tag_prev<num_tag_univ ; tag_prev++){
            
            temp = prob_transition[sub2ind(tag_curr, tag_prev, num_tag_univ)] *
            delta_val[sub2ind(idx-1,tag_prev,num_tag_univ)];
            
            if (temp > max_val){
                max_val = temp;
                max_idx = tag_prev;
            }
        }
        
        delta_val[sub2ind(idx, tag_curr, num_tag_univ)] =
        prob_word_given_tag[sub2ind(word_idx, tag_curr, num_tag_univ)] * max_val;
        delta_maxIdx[sub2ind(idx-1,tag_curr,num_tag_univ)] = max_idx;
        
    }
}



/**********************************<Function related to Indexing>**********************************/

/************************************************************
 Find maximum value and maximum index
 ************************************************************/

void maximum(const vec delta_val, const dictionary idx, real& max_val, dictionary& max_idx,
             const dictionary num_tag_univ){
    
    max_val = neg_inf;
    max_idx = 0;
    real temp = 0;
    
    for (dictionary i=0 ; i<num_tag_univ ; i++){
        
        temp = delta_val[sub2ind(idx, i, num_tag_univ)];
        
        if (temp>max_val){
            max_val = temp;
            max_idx = i;
        }
    }
}

