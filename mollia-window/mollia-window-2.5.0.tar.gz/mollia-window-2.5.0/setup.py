import platform
from setuptools import Extension, setup

# sudo apt install libsdl2-dev

system = platform.system().lower()

include_dirs = {
    'windows': [
        './deps/imgui',
        './deps/imgui/backends',
        './deps/SDL2/include',
    ],
    'linux': [
        './deps/imgui',
        './deps/imgui/backends',
        '/usr/include/SDL2',
    ],
}

library_dirs = {
    'windows': ['./deps/SDL2/lib/x64'],
    'linux': ['/usr/lib/x86_64-linux-gnu/'],
}

libraries = {
    'windows': ['User32', 'Gdi32', 'Shell32', 'OpenGL32', 'SDL2'],
    'linux': ['GL', 'SDL2'],
}

ext = Extension(
    name='mollia_window',
    include_dirs=include_dirs[system],
    library_dirs=library_dirs[system],
    sources=[
        './mollia_window.cpp',
        './deps/imgui/imgui.cpp',
        './deps/imgui/imgui_draw.cpp',
        './deps/imgui/imgui_demo.cpp',
        './deps/imgui/imgui_tables.cpp',
        './deps/imgui/imgui_widgets.cpp',
        './deps/imgui/backends/imgui_impl_sdl.cpp',
        './deps/imgui/backends/imgui_impl_opengl3.cpp',
    ],
    libraries=libraries[system],
    # extra_compile_args=['/Z7'],
    # extra_link_args=['/DEBUG:FULL'],
)

setup(
    name='mollia-window',
    version='2.5.0',
    author='Mollia Zrt.',
    license='MIT',
    ext_modules=[ext],
    packages=['mollia_window-stubs'],
    package_data={'mollia_window-stubs': ['__init__.pyi']},
    data_files=[('.', ['SDL2.dll'])],
    include_package_data=True,
)
