from conans import ConanFile, CMake, tools
import os

class G3logConan(ConanFile):
	name = "g3log"
	version = "master"
	license = "Unlicense"
	url = "https://github.com/Brunni/conan-g3log"
	description = "G3log is an asynchronous, crash safe, logger that is easy to use with default logging sinks or you can add your own."
	settings = "os", "compiler", "build_type", "arch"
	options = {"shared": [True, False]}
	default_options = "shared=False"
	generators = "cmake"
	
	def config(self):
		if self.scope.dev and self.scope.build_tests:
			self.requires( "gtest/1.8.0@lasote/stable" )
			self.options["gtest"].shared = False
		print("Description is: %s" % self.description)
		print("default_option is: %s" % self.default_options)
		print("shared is: %s" % self.options.shared)

	def source(self):
		self.run("git clone --depth 1 https://github.com/KjellKod/g3log.git")
		#self.run("cd hello && git checkout static_shared")
		# This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
		# if the packaged project doesn't have variables to set it properly
		tools.replace_in_file("g3log/CMakeLists.txt", "project (g3log)", '''project (g3log)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

	def build(self):
		cmake = CMake(self.settings)
		cmake_opts = "-DUSE_CONAN=True "
		cmake_opts += "-DADD_G3LOG_UNIT_TEST=True " if self.scope.dev and self.scope.build_tests else ""
		if self.options.shared:
			print("Building shared lib only")
			target = "g3logger_shared"
			cmake_opts += "-DADD_BUILD_WIN_SHARED=True "
		else:
			print("Building static lib only")
			target = "g3logger"
		
		cmake_opts += "-DADD_FATAL_EXAMPLE=OFF "
		self.run('cmake %s/g3log %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts))
		# We need to prevent to build static library as well when building shared. It might overwrite the lib file!
		self.run("cmake --build . %s --target %s" % (cmake.build_config, target))

	def package(self):
		self.copy("*.hpp", dst="include", src="g3log/src")
		self.copy("*.lib", dst="lib", keep_path=False)
		self.copy("*.exp", dst="lib", keep_path=False)
		self.copy("*.dll", dst="bin", keep_path=False) #shared lib
		self.copy("*.so", dst="lib", keep_path=False)
		self.copy("*.a", dst="lib", keep_path=False)

	def package_info(self):
		self.cpp_info.libs = ["g3logger"]
		if self.settings.os == "Linux":
			self.cpp_info.libs.append("pthread")
