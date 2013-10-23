#include <utility>
#include "primes.h"

namespace {
	std::pair<long,long> nextFactors(
		const std::pair<long,long>& previousFactors, long number) {
		long nextFirst = previousFactors.first + 1L;
		long nextSecond;
		for (nextSecond = previousFactors.second;
			(number % nextFirst) != 0 && nextFirst <= nextSecond;
			++nextFirst) {
			nextSecond = number / nextFirst;
		}
		return std::make_pair(nextFirst, nextSecond);
	}
}

bool Math::isPrime(long number) {
	if (number <= 1) {
		return false;
	}

	auto currentFactors = std::make_pair(1L, number);
	currentFactors = nextFactors(currentFactors, number);
	return currentFactors.first >= currentFactors.second;
}
