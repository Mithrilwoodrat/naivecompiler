clang -Xclang -ast-dump -fsyntax-only $1
clang -fsyntax-only -Xclang -analyze -Xclang -analyzer-checker=debug.DumpCFG $1