// should be compiled with c++17
#include <iostream>
#include <ctime>

#define u unsigned

bool is_prime(u int num){
    if (num == 1 || num == 0)
		return false;
	for (int i = 2; i * i <= num; i++)
	{
		if (num % i == 0)
			return false;
	}
	
	return true;
}

std::pair<int, int> generate_prime_numbers(u int low_lim, u int upper_lim){
    u int first_num = 0;
    u int second_num = 0;
    do {
        first_num = low_lim + (rand() % upper_lim);
        second_num = low_lim + (rand() % upper_lim); 
    } while (!is_prime(first_num) || !is_prime(second_num));
    
    return std::make_pair(first_num, second_num);
}

u int phi(u int p, u int q){
    return (p - 1) * (q - 1);
}

u int gcd(u int first, u int second){
    if(first == 0)
		return second;
	else if (second == 0)
		return first;
	else
		return gcd(second, first % second);
}

u int find_coprime(u int phi_res){
    u int e = 2;
    while (e < phi_res){
        u int gcd_res = gcd(e, phi_res);
        if (gcd_res == 1)
            return e;
        e++;
    }
    
    return e;
}

u int calculate_d(u int phi_res, u int e){
    u int k = 1;
    u int d = 0;
    
    while ((((k * phi_res) + 1) % e) != 0)
        k++;
    d = ((k * phi_res) + 1) / e;
    
    return d;
}

int main()
{
    srand(time(0));
    // from 1k to 10k
    auto [p, q] = generate_prime_numbers(1000, 10000);
    long long n = p * q;
    u int phi_res = phi(p, q);
    u int e = find_coprime(phi_res);
    u int d = calculate_d(phi_res, e);
    
    std::cout << "(" << e << "," << " " << n << ") -- public key" << std::endl;
    std::cout << "(" << e << "," << " " << d << ") -- private key";
    /*
    (e, n) pair stands for public key, could be published anywhere
    (e, d) pair stands for private key and keeps in secret
    */
    
    return 0;
}