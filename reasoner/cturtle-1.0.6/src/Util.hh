//
// Copyright 2016 Giovanni Mels
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

#ifndef N3_UTIL_HH
#define N3_UTIL_HH

#include <string>

namespace turtle {

	void useBinaryStreams();
	
	std::string toUri(const std::string &file);
	
	bool exists(const std::string &fileName);
}

#endif /* N3_UTIL_HH */
