#include <stdio.h>
#include <curl/curl.h>

int main(void) {
  // We will assume curl_easy_init is deprecated for this test
  CURL *curl = curl_easy_init();
  return 0;
}
