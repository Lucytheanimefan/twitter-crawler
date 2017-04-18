//
//  main.cpp
//  
//
//
//
//

#include "header.hpp"

/* forward function declarations */
inline void tokenize(char* input[], vec_str& output);

/************************************************************
 Sentence tokenizing function
 ************************************************************/

/* Reference:
 https://docs.python.org/2/extending/embedding.html
 */




void tokenize(char* tweet, vec_str& output){
    //    string tweet "House Intel committee chairman: Were there physical wiretaps of Trump Tower? No, there never was.";
    
    
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    
    /* Set Module Name */
    pName = PyString_FromString("parser");
    
    /* Import Module */
    pModule = PyImport_Import(pName);
    
    /* Garbage Collect : pName */
    Py_DECREF(pName);
    
    /* Import Function */
    pFunc = PyObject_GetAttrString(pModule, "tokenize");
//    Py_INCREF(pFunc);
    
    /* Create Input (represented as Python tuple) */
//    pArgs = PyTuple_New(1);
    pArgs = Py_BuildValue("(s)", tweet);
//    pTweet = PyString_FromString(input[2]);
//    pTweet_len = PyInt_FromSize_t(tweet_len);
    
    /* Set Input Values */
//    PyTuple_SetItem(pArgs, 0, pTweet);
//    PyTuple_SetItem(pArgs, 1, pTweet_len);
//    Py_DECREF(pTweet);
//    Py_DECREF(pTweet_len);
    
//    PyGILState_STATE gstate;
//    gstate = PyGILState_Ensure();
    
    /* Call function */
    pValue = PyObject_CallObject(pFunc, pArgs);
    
//    PyGILState_Release(gstate);
    
    Py_DECREF(pArgs);
    
    for (int i = 0; i < PyList_Size(pValue); i++) {
        //        temp = PyList_GetItem(pValue, i);
        output.push_back(PyString_AsString(PyList_GetItem(pValue, i)));
    }
    
    Py_DECREF(pValue);
    
    //    int count = (int) PyList_Size(pValue);
    //    std::cout<<"Safe"<<std::endl;
    //    float temp[count];
    //    PyObject *ptemp, *objectsRepresentation ;
    //    char* a11;
    //
    //
    //    for (int i = 0 ; i < count ; i++ )
    //    {
    //        ptemp = PyList_GetItem(pValue,i);
    //        objectsRepresentation = PyObject_Repr(ptemp);
    //        a11 = PyString_AsString(objectsRepresentation);
    //        temp[i] = (float)strtod(a11,NULL);
    //    }
    
    //    output = PyString_AsString(pValue);
    //    std::cout<<output<<std::endl;
    
    
    //    PyObject* pStrObj = PyUnicode_AsUTF8String(pValue);
    //    output = PyBytes_AsString(pStrObj);
    //    Py_DECREF(pStrObj);
    
    
    /* Garbage Collect */
    Py_XDECREF(pFunc);
    Py_DECREF(pModule);
    
}

/**********************************<Main function>**********************************/

/************************************************************
 Main function
 ************************************************************/

int main(int argc, char* argv[]){
    
    /******************
     Dictionary
     ******************/
    /* Load tag dictionary */
    hashtable tagList_by_tag;
    vec_str tagList_by_idx;
    load_dictionary(tagList_by_tag, tagList_by_idx, "tag_univ");
    dictionary num_tag_univ = (dictionary)tagList_by_tag.size();
    
    /* Load word dictionary */
    hashtable wordList_by_word;
    vec_str wordList_by_idx;
    load_dictionary(wordList_by_word, wordList_by_idx, "word_univ");
    dictionary num_word_univ = (dictionary)wordList_by_word.size();
    
    
    /******************
     HMM parameters
     ******************/
    /* File name variable */
    string filename;
    
    /* Load parameters for HMM */
    // P(tag), tag:column*/
    vec prob_tag;
    prob_tag.resize(num_tag_univ);
    filename = "prob_tag";
    load_param(prob_tag, 1, num_tag_univ, filename);
    //save_param(prob_tag, 1, num_tag_univ, filename);

    // P(word | tag), word:row, tag:column
    vec prob_word_given_tag;
    prob_word_given_tag.resize(num_word_univ * num_tag_univ);
    filename = "prob_word_given_tag";
    load_param(prob_word_given_tag, num_word_univ, num_tag_univ, filename);
    //save_param(prob_word_given_tag, num_word_univ, num_tag_univ, filename);

    // P(tag_curr | tag_prev), tag_curr:row, tag_prev:column
    vec prob_transition;
    prob_transition.resize(num_tag_univ * num_tag_univ);
    filename = "prob_transition";
    load_param(prob_transition, num_tag_univ, num_tag_univ, filename);
    //save_param(prob_transition, num_tag_univ, num_tag_univ, filename);
    
    
    /******************
     Python Setting
     ******************/
    /* Set Python Path */
    setenv("PYTHONPATH",".",1);
    
    /* Start Python Interpreter */
    Py_Initialize();
    
    /* Import necessary Python Library */
//    PyRun_SimpleString("from nltk import word_tokenize");
    char* tweet = (char*) argv[0];

    //"The building houses many people.";
    
    //"The building houses many people."
    
    //"House Intel committee chairman: Were there physical wiretaps of Trump Tower? No, there never was.";
    //"With Backing of Law Enforcement, an Undocumented Immigrant Gets a Reprieve";
    //"People ate delicious beef while sitting in the table";
    
    
    vec_str token;
    vec_idx word;
    vec_idx tag;
    
    tokenize(tweet, token);
    
    /* End Python Interpreter */
    Py_Finalize();
    

    int n = (int)token.size();
    word.resize(n);
    tag.resize(n);
    
    /* Find word idx of each word in the token, using dictionary */
    lookup_word_dictionary(token, word, wordList_by_word);
    
    
    /* Bigram tagging, using Viterbi algirhtm. The result is stored in "tag" */
    viterbi(word, tag, prob_tag, prob_word_given_tag, prob_transition, num_tag_univ);
    
    
    for(int i=0; i<n ;i++){
        std::cout<<token[i]<<":"<<tagList_by_idx[tag[i]]<<std::endl;
    }
    
    std::cout<<wordList_by_word.find("law")->second;

    vec_str word_output;
    vec freq;
    //return [("Orange", "Pineapple"), (3,1)]


    return 0;
}











