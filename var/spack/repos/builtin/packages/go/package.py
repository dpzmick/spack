# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re

import llnl.util.tty as tty

from spack.package import *

# - vanilla CentOS 7, and possibly other systems, fail a test:
#   TestCloneNEWUSERAndRemapRootDisableSetgroups
#
#   The Fix, discussed here: https://github.com/golang/go/issues/16283
#   is to enable "user_namespace".
#
#   On a Digital Ocean image, this can be achieved by updating
#   `/etc/default/grub` so that the `GRUB_CMDLINE_LINUX` variable
#   includes `user_namespace.enable=1`, re-cooking the grub
#   configuration with `sudo grub2-mkconfig -o /boot/grub2/grub.cfg`,
#   and then rebooting.
#
# - on CentOS 7 systems (and possibly others) you need to have the
#   glibc package installed or various static cgo tests fail.
#
# - When building on a *large* machine (144 cores, 1.5TB RAM) I need
#   to run `ulimit -u 8192` to bump up the max number of user processes.
#   Failure to do so results in an explosion in one of the tests and an
#   epic stack trace....


class Go(Package):
    """The golang compiler and build environment"""

    homepage = "https://golang.org"
    url = "https://dl.google.com/go/go1.16.6.src.tar.gz"
    git = "https://go.googlesource.com/go.git"

    extendable = True
    executables = ["^go$"]

    maintainers = ["alecbcs"]

    version("1.19.4", sha256="eda74db4ac494800a3e66ee784e495bfbb9b8e535df924a8b01b1a8028b7f368")
    version("1.18", sha256="38f423db4cc834883f2b52344282fa7a39fbb93650dc62a11fdf0be6409bdad6")
    version("1.17.8", sha256="2effcd898140da79a061f3784ca4f8d8b13d811fb2abe9dad2404442dabbdf7a")
    version("1.17.7", sha256="c108cd33b73b1911a02b697741df3dea43e01a5c4e08e409e8b3a0e3745d2b4d")
    version(
        "1.17.3",
        sha256="705c64251e5b25d5d55ede1039c6aa22bea40a7a931d14c370339853643c3df0",
        deprecated=True,
    )
    version(
        "1.17.2",
        sha256="2255eb3e4e824dd7d5fcdc2e7f84534371c186312e546fb1086a34c17752f431",
        deprecated=True,
    )
    version(
        "1.17.1",
        sha256="49dc08339770acd5613312db8c141eaf61779995577b89d93b541ef83067e5b1",
        deprecated=True,
    )
    version(
        "1.17",
        sha256="3a70e5055509f347c0fb831ca07a2bf3b531068f349b14a3c652e9b5b67beb5d",
        deprecated=True,
    )
    version("1.16.10", sha256="a905472011585e403d00d2a41de7ced29b8884309d73482a307f689fd0f320b5")
    version("1.16.9", sha256="0a1cc7fd7bd20448f71ebed64d846138850d5099b18cf5cc10a4fc45160d8c3d")
    version("1.16.6", sha256="a3a5d4bc401b51db065e4f93b523347a4d343ae0c0b08a65c3423b05a138037d")
    version("1.16.5", sha256="7bfa7e5908c7cc9e75da5ddf3066d7cbcf3fd9fa51945851325eebc17f50ba80")
    version("1.16.4", sha256="ae4f6b6e2a1677d31817984655a762074b5356da50fb58722b99104870d43503")
    version("1.16.3", sha256="b298d29de9236ca47a023e382313bcc2d2eed31dfa706b60a04103ce83a71a25")
    version("1.16.2", sha256="37ca14287a23cb8ba2ac3f5c3dd8adbc1f7a54b9701a57824bf19a0b271f83ea")
    version("1.16", sha256="7688063d55656105898f323d90a79a39c378d86fe89ae192eb3b7fc46347c95a")
    version("1.15.13", sha256="99069e7223479cce4553f84f874b9345f6f4045f27cf5089489b546da619a244")
    version("1.15.12", sha256="1c6911937df4a277fa74e7b7efc3d08594498c4c4adc0b6c4ae3566137528091")
    version("1.15.11", sha256="f25b2441d4c76cf63cde94d59bab237cc33e8a2a139040d904c8630f46d061e5")
    version("1.15.8", sha256="540c0ab7781084d124991321ed1458e479982de94454a98afab6acadf38497c2")
    version("1.15.7", sha256="8631b3aafd8ecb9244ec2ffb8a2a8b4983cf4ad15572b9801f7c5b167c1a2abc")
    version("1.15.6", sha256="890bba73c5e2b19ffb1180e385ea225059eb008eb91b694875dd86ea48675817")
    version("1.15.5", sha256="c1076b90cf94b73ebed62a81d802cd84d43d02dea8c07abdc922c57a071c84f1")
    version("1.15.2", sha256="28bf9d0bcde251011caae230a4a05d917b172ea203f2a62f2c2f9533589d4b4d")
    version("1.15.1", sha256="d3743752a421881b5cc007c76b4b68becc3ad053e61275567edab1c99e154d30")
    version("1.15", sha256="69438f7ed4f532154ffaf878f3dfd83747e7a00b70b3556eddabf7aaee28ac3a")
    version("1.14.14", sha256="6204bf32f58fae0853f47f1bd0c51d9e0ac11f1ffb406bed07a0a8b016c8a76f")
    version("1.14.13", sha256="ba1d244c6b5c0ed04aa0d7856d06aceb89ed31b895de6ff783efb1cc8ab6b177")
    version("1.14.12", sha256="b34f4b7ad799eab4c1a52bdef253602ce957125a512f5a1b28dce43c6841b971")
    version("1.14.9", sha256="c687c848cc09bcabf2b5e534c3fc4259abebbfc9014dd05a1a2dc6106f404554")
    version("1.14.8", sha256="d9a613fb55f508cf84e753456a7c6a113c8265839d5b7fe060da335c93d6e36a")
    version("1.14.6", sha256="73fc9d781815d411928eccb92bf20d5b4264797be69410eac854babe44c94c09")
    version("1.14.5", sha256="ca4c080c90735e56152ac52cd77ae57fe573d1debb1a58e03da9cc362440315c")
    version("1.14.4", sha256="7011af3bbc2ac108d1b82ea8abb87b2e63f78844f0259be20cde4d42c5c40584")
    version("1.14.3", sha256="93023778d4d1797b7bc6a53e86c3a9b150c923953225f8a48a2d5fabc971af56")
    version("1.14.2", sha256="98de84e69726a66da7b4e58eac41b99cbe274d7e8906eeb8a5b7eb0aadee7f7c")
    version("1.14.1", sha256="2ad2572115b0d1b4cb4c138e6b3a31cee6294cb48af75ee86bec3dca04507676")
    version("1.14", sha256="6d643e46ad565058c7a39dac01144172ef9bd476521f42148be59249e4b74389")
    version("1.13.14", sha256="197333e97290e9ea8796f738d61019dcba1c377c2f3961fd6a114918ecc7ab06")
    version("1.13.13", sha256="ab7e44461e734ce1fd5f4f82c74c6d236e947194d868514d48a2b1ea73d25137")
    version("1.13.12", sha256="17ba2c4de4d78793a21cc659d9907f4356cd9c8de8b7d0899cdedcef712eba34")
    version("1.13.11", sha256="89ed1abce25ad003521c125d6583c93c1280de200ad221f961085200a6c00679")
    version("1.13.10", sha256="eb9ccc8bf59ed068e7eff73e154e4f5ee7eec0a47a610fb864e3332a2fdc8b8c")
    version("1.13.9", sha256="34bb19d806e0bc4ad8f508ae24bade5e9fedfa53d09be63b488a9314d2d4f31d")
    version("1.13.8", sha256="b13bf04633d4d8cf53226ebeaace8d4d2fd07ae6fa676d0844a688339debec34")
    version("1.13.7", sha256="e4ad42cc5f5c19521fbbbde3680995f2546110b5c6aa2b48c3754ff7af9b41f4")
    version("1.13.6", sha256="aae5be954bdc40bcf8006eb77e8d8a5dde412722bc8effcdaf9772620d06420c")
    version("1.13.5", sha256="27d356e2a0b30d9983b60a788cf225da5f914066b37a6b4f69d457ba55a626ff")
    version("1.13.4", sha256="95dbeab442ee2746b9acf0934c8e2fc26414a0565c008631b04addb8c02e7624")
    version("1.13.3", sha256="4f7123044375d5c404280737fbd2d0b17064b66182a65919ffe20ffe8620e3df")
    version("1.13.2", sha256="1ea68e01472e4276526902b8817abd65cf84ed921977266f0c11968d5e915f44")
    version("1.13.1", sha256="81f154e69544b9fa92b1475ff5f11e64270260d46e7e36c34aafc8bc96209358")
    version("1.13", sha256="3fc0b8b6101d42efd7da1da3029c0a13f22079c0c37ef9730209d8ec665bf122")
    version("1.12.17", sha256="de878218c43aa3c3bad54c1c52d95e3b0e5d336e1285c647383e775541a28b25")
    version("1.12.15", sha256="8aba74417e527524ad5724e6e6c21016795d1017692db76d1b0851c6bdec84c3")
    version("1.12.14", sha256="39dbf05f7e2ffcb19b08f07d53dcc96feadeb1987fef9e279e7ff0c598213064")
    version("1.12.13", sha256="5383d3b8db4baa48284ffcb14606d9cad6f03e9db843fa6d835b94d63cccf5a7")
    version("1.12.12", sha256="fcb33b5290fa9bcc52be3211501540df7483d7276b031fc77528672a3c705b99")
    version("1.12.11", sha256="fcf58935236802929f5726e96cd1d900853b377bec2c51b2e37219c658a4950f")
    version("1.12.10", sha256="f56e48fce80646d3c94dcf36d3e3f490f6d541a92070ad409b87b6bbb9da3954")
    version("1.12.9", sha256="ab0e56ed9c4732a653ed22e232652709afbf573e710f56a07f7fdeca578d62fc")
    version("1.12.8", sha256="11ad2e2e31ff63fcf8a2bdffbe9bfa2e1845653358daed593c8c2d03453c9898")
    version("1.12.6", sha256="c96c5ccc7455638ae1a8b7498a030fe653731c8391c5f8e79590bce72f92b4ca")
    version("1.12.5", sha256="2aa5f088cbb332e73fc3def546800616b38d3bfe6b8713b8a6404060f22503e8")
    version("1.11.13", sha256="5032095fd3f641cafcce164f551e5ae873785ce7b07ca7c143aecd18f7ba4076")
    version("1.11.11", sha256="1fff7c33ef2522e6dfaf6ab96ec4c2a8b76d018aae6fc88ce2bd40f2202d0f8c")
    version("1.11.10", sha256="df27e96a9d1d362c46ecd975f1faa56b8c300f5c529074e9ea79bdd885493c1b")
    version("1.11.5", sha256="bc1ef02bb1668835db1390a2e478dcbccb5dd16911691af9d75184bbe5aa943e")
    version("1.11.4", sha256="4cfd42720a6b1e79a8024895fa6607b69972e8e32446df76d6ce79801bbadb15")
    version("1.11.2", sha256="042fba357210816160341f1002440550e952eb12678f7c9e7e9d389437942550")
    version("1.11.1", sha256="558f8c169ae215e25b81421596e8de7572bd3ba824b79add22fba6e284db1117")
    version("1.11", sha256="afc1e12f5fe49a471e3aae7d906c73e9d5b1fdd36d52d72652dde8f6250152fb")
    version("1.10.3", sha256="567b1cc66c9704d1c019c50bef946272e911ec6baf244310f87f4e678be155f2")
    version("1.10.2", sha256="6264609c6b9cd8ed8e02ca84605d727ce1898d74efa79841660b2e3e985a98bd")
    version("1.10.1", sha256="589449ff6c3ccbff1d391d4e7ab5bb5d5643a5a41a04c99315e55c16bbf73ddc")
    version("1.9.5", sha256="f1c2bb7f32bbd8fa7a19cc1608e0d06582df32ff5f0340967d83fb0017c49fbc")
    version("1.9.2", sha256="665f184bf8ac89986cfd5a4460736976f60b57df6b320ad71ad4cef53bb143dc")
    version("1.9.1", sha256="a84afc9dc7d64fe0fa84d4d735e2ece23831a22117b50dafc75c1484f1cb550e")
    version("1.9", sha256="a4ab229028ed167ba1986825751463605264e44868362ca8e7accc8be057e993")
    version("1.8.3", sha256="5f5dea2447e7dcfdc50fa6b94c512e58bfba5673c039259fd843f68829d99fa6")
    version("1.8.1", sha256="33daf4c03f86120fdfdc66bddf6bfff4661c7ca11c5da473e537f4d69b470e57")
    version("1.8", sha256="406865f587b44be7092f206d73fc1de252600b79b3cacc587b74b5ef5c623596")
    version("1.7.5", sha256="4e834513a2079f8cbbd357502cccaac9507fd00a1efe672375798858ff291815")
    version("1.7.4", sha256="4c189111e9ba651a2bb3ee868aa881fab36b2f2da3409e80885ca758a6b614cc")
    version("1.6.4", sha256="8796cc48217b59595832aa9de6db45f58706dae68c9c7fbbd78c9fdbe3cd9032")

    provides("golang")

    depends_on("git", type=("build", "link", "run"))

    # aarch64 machines (including Macs with Apple silicon) can't use
    # go-bootstrap because it pre-dates aarch64 support in Go.  These machines
    # have to rely on Go support in gcc (which may require compiling a version
    # of gcc with Go support just to satisfy this requirement) or external go:

    # #27769: On M1/MacOS, platform.machine() may return arm64:
    if platform.machine() in ["arm64", "aarch64"]:
        # Use an external go compiler from packages.yaml/`spack external find go-bootstrap`,
        # but fallback to build go-bootstrap@1.4 or to gcc with languages=go (for aarch64):
        depends_on("go-external-or-gccgo-bootstrap", type="build")
    else:
        depends_on("go-bootstrap", type="build")

    # https://github.com/golang/go/issues/17545
    patch("time_test.patch", when="@1.6.4:1.7.4")

    # https://github.com/golang/go/issues/17986
    # The fix for this issue has been merged into the 1.8 tree.
    patch("misc-cgo-testcshared.patch", level=0, when="@1.6.4:1.7.5")

    # Unrecognized option '-fno-lto'
    conflicts("%gcc@:4", when="@1.17:")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"go version go(\S+)", output)
        return match.group(1) if match else None

    # NOTE: Older versions of Go attempt to download external files that have
    # since been moved while running the test suite.  This patch modifies the
    # test files so that these tests don't cause false failures.
    # See: https://github.com/golang/go/issues/15694
    @when("@:1.4.3")
    def patch(self):
        test_suite_file = FileFilter(join_path("src", "run.bash"))
        test_suite_file.filter(
            r"^(.*)(\$GOROOT/src/cmd/api/run.go)(.*)$",
            r"# \1\2\3",
        )

    def install(self, spec, prefix):
        bash = which("bash")

        wd = "."

        # 1.11.5 directory structure is slightly different
        if self.version == Version("1.11.5"):
            wd = "go"

        with working_dir(join_path(wd, "src")):
            bash("{0}.bash".format("all" if self.run_tests else "make"))

        install_tree(wd, prefix)

    def setup_build_environment(self, env):
        env.set("GOROOT_FINAL", self.spec.prefix)
        # We need to set CC/CXX_FOR_TARGET, otherwise cgo will use the
        # internal Spack wrappers and fail.
        env.set("CC_FOR_TARGET", self.compiler.cc)
        env.set("CXX_FOR_TARGET", self.compiler.cxx)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before go modules' install() methods.

        In most cases, extensions will only need to set GOPATH and use go::

        env['GOPATH'] = self.source_path + ':' + env['GOPATH']
        go('get', '<package>', env=env)
        install_tree('bin', prefix.bin)
        """
        #  Add a go command/compiler for extensions
        module.go = self.spec["go"].command

    def generate_path_components(self, dependent_spec):
        if os.environ.get("GOROOT", False):
            tty.warn("GOROOT is set, this is not recommended")

        # Set to include paths of dependencies
        path_components = [dependent_spec.prefix]
        for d in dependent_spec.traverse():
            if d.package.extends(self.spec):
                path_components.append(d.prefix)
        return ":".join(path_components)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # This *MUST* be first, this is where new code is installed
        env.prepend_path("GOPATH", self.generate_path_components(dependent_spec))

    def setup_dependent_run_environment(self, env, dependent_spec):
        # Allow packages to find this when using module files
        env.prepend_path("GOPATH", self.generate_path_components(dependent_spec))
