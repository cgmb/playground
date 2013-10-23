#include <iostream>
#include <cerrno>
#include <cstdlib>

int main(int argc, char* argv[]) {
	if (argc < 2) {
		std::cerr << "Insufficient arguments. Please enter an integer" << std::endl;
		return 1;
	} else if (argc > 2) {
		std::cerr << "Too many arguments. Please enter an integer" << std::endl;
		return 2;
	}

	char* end;
	long number = strtol(argv[1], &end, 10);
	if (*end != '\0' || errno == EINVAL) {
		std::cerr << "\"" << argv[1] << "\" is not an integer." << std::endl;
		return 3;
	} else if (errno == ERANGE) {
		std::cerr << "Given integer is too large." << std::endl;
		return 4;
	}

	return 0;
}