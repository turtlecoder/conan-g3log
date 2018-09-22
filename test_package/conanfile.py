from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "local")
username = os.getenv("CONAN_USERNAME", "user")


class G3logTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "g3log/master@%s/%s" % (username, channel)
    generators = "cmake"

    def configure(self):
        print("Testing shared library: %s" % self.options["g3log"].shared)

    def build(self):
        cmake = CMake(self)
        self.run('cmake "%s" %s' % (self.source_folder, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "bin")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
