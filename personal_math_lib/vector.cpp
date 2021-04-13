#include <iostream>
#include <vector>

//template for vector
template<typename T>
std::vector<double> vector_impl(const T& t)
{   
    return t;
}

//function that takes in any number of vector and returns a vector of those vectors
template<typename ... Param>
std::vector<std::vector<double>> vector_holder(const Param& ... param)
{   
    return {vector_impl(param)...};
}

//function that takes in vector of vectors and adds them
std::vector<double> vector_addition(std::vector<std::vector<double>> vecs)
{   
    std::vector<double> result = {};
    for (int i=0; i < vecs[0].size(); i++)
    {   
        result.push_back(0);
    }
    
    for (int i=0; i < vecs.size(); i++)
    {
        //TODO add safety check for size
        for (int j=0; j < vecs[0].size(); j++)
        {
            result[j] += vecs[i][j];
        }
    }
    return result;
}

std::vector<double> scalar_multiplication(std::vector<double> v, double scalar) 
{
    std::vector<double> scaled_vector = {};   
    for (double i = 0; i < v.size(); i++)
    {
        scaled_vector.push_back(scalar * v[i]);
    }
    return scaled_vector;
}

//std::vector<double> vector_addition

int main()
{
    /* --Scalar Multiplication
    std::vector<double> test = {1,2,3};
    std::vector<double> result;
    
    result = scalar_multiplication(test, 3);
    for (double i = 0; i < result.size(); i++){
        std::cout << result[i] << std::endl;
    }*/

    /* --Vector addition */
    std::vector<double> v1 = {1,2,3};
    std::vector<double> v2 = {4,5,6};
    auto vec = vector_holder(v1,v2);
    auto vec2 = vector_addition(vec);

    for (int i = 0; i < vec2.size(); i++)
    {
        std::cout << vec2[i] << "\n";
    }
    return 0;
}
