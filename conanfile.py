from conans import ConanFile, CMake, tools
import os


class G3logConan(ConanFile):
    name = "g3log"
    version = "master"
    license = "MIT"
    url = "https://github.com/oskargargas/conan-g3log"
    source_url = "https://github.com/KjellKod/g3log"
    commit = "master"
    description = "G3log is an asynchronous, crash safe, logger that is easy to use with default logging sinks or you can add your own."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "debug": [True, False],
               "dev": [True, False],
               "build_tests": [True, False]}
    default_options = ("shared=False",
                       "debug=False",
                       "build_tests=True",
                       "dev=True")
    generators = "cmake"
    requires = "gtest/1.8.0@bincrafters/stable"
    
    # def config(self):
    #     if self.scope.dev and self.scope.build_tests:
    #         self.requires("gtest/1.8.0@lasote/stable")
    #         self.options["gtest"].shared = False
    def configure(self):
        # if not(self.options.dev and self.options.build_test):
        #     # self.requires.remove("gtest/1.8.0@bincrafters/stable")
        pass


    def config_options(self):
        pass

    def source(self):
        if not os.path.isdir('g3log'):
            self.run('git clone %s g3log' % self.source_url)
        else:
            self.run('cd g3log && git fetch origin')

        self.run('cd g3log && git checkout %s' % self.commit)

        tools.replace_in_file("g3log/CMakeLists.txt", "project (g3log)", '''project (g3log)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self.settings)

        cmake_opts = "-DADD_G3LOG_UNIT_TEST=True " if self.scope.dev and self.scope.build_tests else ""
        cmake_opts += "-DBUILD_EXAMPLES:BOOL=False "
        cmake_opts += "-DADD_FATAL_EXAMPLE=OFF "
        if self.settings.os == "Macos":
            cmake_opts += "-DCMAKE_SKIP_RPATH:BOOL=ON "

        if self.options.shared:
            target = "g3logger_shared"
            cmake_opts += "-DADD_BUILD_WIN_SHARED=True "
        else:
            target = "g3logger"

        self.run('cmake "%s/g3log" %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts))
        self.run('cmake --build . %s --target %s' % (cmake.build_config, target))

    def package(self):
        self.copy("*.hpp", dst="include", src="g3log/src")
        self.copy("*.hpp", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.exp", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["g3logger"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
