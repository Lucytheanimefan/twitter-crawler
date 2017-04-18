//
//  resourceFunc.cpp
//  
//
//
//
//

/* Reference :
 http://www.cplusplus.com/doc/tutorial/files/
 */

#include "header.hpp"

//void load_tag_dictionary(hashtable& tagList_by_tag, vec_str& tagList_by_idx){
///* Reference :
// http://www.nltk.org/_modules/nltk/tag/mapping.html : simplified universal tagset
// */
//    
////    std::ifstream f("./resources/tag_univ.txt");
////    
////    string colon(":");
////    size_t colon_pos;
////    string space(" ");
////    
////    string line;
////    string tag;
////    pair element;
////    dictionary idx_count=0;
////    
////    if (f.is_open()){
////        while(getline(f,line,'\n')){
////            if(0==line.find(space)){
////                continue;
////            }
////            else{
////                colon_pos = line.find_last_of(colon);
////                tag = line.substr(0, colon_pos);
////                element = std::make_pair(tag, idx_count);
////                tagList_by_tag.insert(element);
////                tagList_by_idx.push_back(tag);
////                idx_count++;
////            }
////        }
////        f.close();
////    }
////    else{
////        std::cout << "Unable to load file";
////    }
//    
//    std::ifstream f("./resources/tag_univ.txt");
//    
//    string line;
//    pair element;
//    dictionary idx_count=0;
//    
//    if (f.is_open()){
//        while(getline(f,line,'\n')){
//            element = std::make_pair(line, idx_count);
//            tagList_by_tag.insert(element);
//            tagList_by_idx.push_back(line);
//            idx_count++;
//        }
//        f.close();
//    }
//    else{
//        std::cout << "Unable to load file";
//    }
//}

//void load_word_dictionary(hashtable& wordList_by_word, vec_str& wordList_by_idx){
//    
//    std::ifstream f("./resources/word_univ.txt");
//    
//    string line;
//    pair element;
//    dictionary idx_count=0;
//    
//    if (f.is_open()){
//        while(getline(f,line,'\n')){
//            element = std::make_pair(line, idx_count);
//            wordList_by_word.insert(element);
//            wordList_by_idx.push_back(line);
//            idx_count++;
//        }
//        f.close();
//    }
//    else{
//        std::cout << "Unable to load file";
//    }
//}

void load_dictionary(hashtable& List_by_str, vec_str& List_by_idx, const string filename){
    
    string path = "./resources/"+filename+".txt";
    
    std::ifstream f(path);
    
    string line;
    pair element;
    dictionary idx_count=0;
    
    if (f.is_open()){
        while(getline(f,line,'\n')){
            element = std::make_pair(line, idx_count);
            List_by_str.insert(element);
            List_by_idx.push_back(line);
            idx_count++;
        }
        f.close();
    }
    else{
        std::cout << "Unable to load file";
    }
}


void load_param(vec& prob, const dictionary num_row, const dictionary num_col, const string filename){

    string path = "./resources/"+filename+".txt";
    
    std::ifstream f(path);
    
    dictionary len = num_row * num_col;

    if (f.is_open()){
        
        for( dictionary idx=0; idx<len; idx++){
            f >> prob[idx];
        }
        f.close();
    }
    else{
        std::cout << "Unable to load file";
    }
    
}


//void save_param(vec prob, dictionary num_row, dictionary num_col, string filename){
//    
//    std:: ofstream f(filename);
//    
//    dictionary len = num_row * num_col;
//    
//    assert(prob.size()==len);
//
//    if(f.is_open()){
//        for (dictionary i = 0; i < num_row; i++){
//            for (dictionary j = 0; j < num_col; j++){
//                if(j!=num_col-1) f << prob[sub2ind(i,j,num_col)]<<" ";
//                else f << prob[sub2ind(i,j,num_col)];
//            }
//            
//            if(i!=num_row-1) f << "\n";
//        }
//        f.close();
//    }
//    else{
//        std::cout << "Unable to save file";
//    }
//}


//int main(int argc, char* argv[]){
//    
//    string filename;
//    
//    /* tag list */
//    vec_str tagList;
//    load_tag_dictionary(tagList);
//    dictionary num_tag_univ = (dictionary)tagList.size();
//    
//    /* word list */
//    vec_str wordList;
//    load_word_dictionary(wordList);
//    dictionary num_word_univ = (dictionary)wordList.size();
//    
//
////    std::cout<< wordList.size() <<std::endl;
////
////    for(int i=0; i<wordList.size(); i++){
////        std::cout<< wordList[i] <<std::endl;
////    }
//    
//    /* load param for HMM */
//    vec prob_tag;
//    prob_tag.resize(num_tag_univ);
//    filename = "./resources/prob_tag.txt";
//    load_param(prob_tag, 1, num_tag_univ, filename);
//    //save_param(prob_tag, 1, num_tag_univ, filename);
//    
//    vec prob_word_given_tag;
//    prob_word_given_tag.resize(num_word_univ * num_tag_univ);
//    filename = "./resources/prob_word_given_tag.txt";
//    load_param(prob_word_given_tag, num_word_univ, num_tag_univ, filename);
//    //save_param(prob_word_given_tag, num_word_univ, num_tag_univ, filename);
//    
//    
//    vec prob_transition;
//    prob_transition.resize(num_tag_univ * num_tag_univ);
//    filename = "./resources/prob_transition.txt";
//    load_param(prob_transition, num_tag_univ, num_tag_univ, filename);
//    //save_param(prob_transition, num_tag_univ, num_tag_univ, filename);
//    
////        for(int i=0; i<prob_word_given_tag.size(); i++){
////            std::cout<< prob_word_given_tag[i] <<std::endl;
////        }
//    
//    return 0;
//}
