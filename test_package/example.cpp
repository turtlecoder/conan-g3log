#include <iostream>
#include <memory>

using namespace std;

#include "g3log/g3log.hpp"
#include "g3log/logworker.hpp"

int main(int argc, char **argv) {
	auto worker = g3::LogWorker::createLogWorker();
	char* log_prefix = argv[0];
	auto defaultHandler = worker->addDefaultLogger(log_prefix, "./");
	g3::initializeLogging(worker.get());
	LOG(DEBUG) << "Log something";
	
    return 0;
}
