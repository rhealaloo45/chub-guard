#include <openai/package>
#include <iostream>

int main() {
    // Strategy 3 should scan this and find the deprecated pattern
    auto response = openai.ChatCompletion.create();
    std::cout << "Running test" << std::endl;
    return 0;
}
