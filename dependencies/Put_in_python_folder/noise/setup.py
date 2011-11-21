from distutils.core import setup, Extension

CFLAGS=[
    "-DMACOSX",
    "-DAPPLE_RUNTIME",
    "-no-cpp-precomp",
    "-Wno-long-double",
    "-g",

    # Loads of warning flags
    "-Wall", "-Wstrict-prototypes", "-Wmissing-prototypes",
    "-Wformat=2", "-W", "-Wshadow",
    "-Wpointer-arith", #"-Wwrite-strings",
    "-Wmissing-declarations",
    "-Wnested-externs",
    "-Wno-long-long",
    "-Wno-import",
    
    # Universal binary flags
    "-arch", "i386",
    "-arch", "ppc",
    "-isysroot", "/Developer/SDKs/MacOSX10.4u.sdk",
    ]

BASE_LDFLAGS = [
    # Universal binary flags
    "-arch", "i386",
    "-arch", "ppc",
    "-isysroot", "/Developer/SDKs/MacOSX10.4u.sdk",
]

module = Extension("_noise", sources = ["_noise.c"], 
    extra_compile_args=CFLAGS, extra_link_args=BASE_LDFLAGS)

setup (name = "noise",
       version = "1.0",
       author = "Malcolm Kesson",
       description = "Perlin noise function.",
       ext_modules = [module])