//
//  test.cpp
//  
//
//  Created by Minwoo Kim on 2017. 4. 4..
//
//

#include <stdio.h>
#include <iostream>
#include <boost/tokenizer.hpp>
#include <string>

int main(){
    using namespace std;
    using namespace boost;
    string s = "This is,  a test";
    tokenizer<> tok(s);
    for(tokenizer<>::iterator beg=tok.begin(); beg!=tok.end();++beg){
        cout << *beg << "\n";
    }
}
