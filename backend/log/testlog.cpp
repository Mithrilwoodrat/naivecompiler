#define DEBUG 1
#include "Logging.h"

using namespace naivecompiler;
int main() {
    Log::InitLogging(LOG_INFO);
    LOG(LOG_DEBUG) << "test DEBUG" << "\n";
    LOG(LOG_INFO) << "test INFO" << "\n";
    LOG(LOG_WARNING) << "test WARNING" << "\n";
    DLOG(LOG_WARNING) << "test Debug Log WARNING" << "\n";
    return 0;
}