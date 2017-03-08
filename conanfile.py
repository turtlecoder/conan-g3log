from conans import ConanFile, CMake, tools
import os


class G3logConan(ConanFile):
	name = "g3log"
	version = "master"
	license = "Unlicense"
	url = "<Package recipe repository url here, for issues about the package>"
	settings = "os", "compiler", "build_type", "arch"
	options = {"shared": [True, False]}
	default_options = "shared=False"
	generators = "cmake"
	
	def config(self):
		if self.scope.dev and self.scope.build_tests:
			self.requires( "gtest/1.8.0@lasote/stable" )
			self.options["gtest"].shared = False

	def source(self):
		self.run("git clone --depth 1 https://github.com/KjellKod/g3log.git")
		#self.run("cd hello && git checkout static_shared")
		# This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
		# if the packaged project doesn't have variables to set it properly
		tools.replace_in_file("g3log/CMakeLists.txt", "PROJECT(g3log)", '''PROJECT(g3log)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

	def build(self):
		cmake = CMake(self.settings)
		cmake_opts = "-DUSE_CONAN=True "
		cmake_opts += "-DADD_G3LOG_UNIT_TEST=True " if self.scope.dev and self.scope.build_tests else ""
		cmake_opts += "-DBUILD_SHARED_LIBS=ON " if self.options.shared else ""
		self.run('cmake %s/g3log %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts))
		self.run("cmake --build . %s" % cmake.build_config)

	def package(self):
		self.copy("*.hpp", dst="include", src="g3log/src")
		self.copy("*.lib", dst="lib", src="Release", keep_path=False)
		self.copy("*.lib", dst="lib", src="Debug", keep_path=False)
		#self.copy("*.dll", dst="bin", keep_path=False) #no shared lib
		self.copy("*.so", dst="lib", src="Release", keep_path=False)
		self.copy("*.a", dst="lib", src="Debug", keep_path=False)

	def package_info(self):
		self.cpp_info.libs = ["g3logger"]
