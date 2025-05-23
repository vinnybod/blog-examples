load("@rules_jvm_external//:defs.bzl", "maven_install")

artifacts = [
    "com.google.guava:guava:31.1-jre",
]

def _deps():
    maven_install(
        name = "maven",
        artifacts = artifacts,
        repositories = [
            "https://repo.maven.apache.org/maven2",
        ],
        maven_install_json = "maven_install.json",
    )

deps = module_extension(lambda ctx: _deps())
