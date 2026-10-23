#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if [ ! -x .venv/bin/python ]; then uv venv .venv --python 3.12; fi
uv pip install --python .venv/bin/python -r requirements.lock.txt
mkdir -p build
case "$(uname -s)" in
 Darwin)
  task_prefix=$(brew --prefix)
  cc -O3 -shared -fPIC src/fill.c -o build/fill.dylib
  cc -O3 -shared -fPIC -I"$task_prefix/include/suitesparse" src/cholmod_bench.c -L"$task_prefix/lib" -Wl,-rpath,"$task_prefix/lib" -lcholmod -o build/cholmod_bench.dylib
  ;;
 Linux)
  cc -O3 -shared -fPIC src/fill.c -o build/fill.so
  cc -O3 -shared -fPIC -I/usr/include/suitesparse src/cholmod_bench.c -lcholmod -o build/cholmod_bench.so
  ln -sf fill.so build/fill.dylib
  ln -sf cholmod_bench.so build/cholmod_bench.dylib
  ;;
 *) echo 'Supported build targets: macOS and Linux' >&2; exit 1 ;;
esac

.venv/bin/python tools/fetch_inputs.py
