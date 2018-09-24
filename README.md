# NaiveCompiler

### A hobby C compiler created in Python and LLVM

## Docker

### Build

```
cd Docker
docker build -t naivescript .
```

### Run

`docker run -i -t naivescript:latest /opt/naivecompiler/test.sh`

## 使用方法

使用 `python2 compiler.py <input>` 显示 AST

使用 `python2 compiler.py <input> -o <output>` 生成 obj

使用 `ld -e <symbol>` 将 obj 文件 链接为 ELF， 并指定 <symbol> 为 entry point。（由于未给 naivecompiler 实现 crt， entry point 的函数不能返回参数，只能设置为 void)

可以使用 ld 链接上 ld，然后就可以调用 glibc 的函数了。crt 问题可以链接上 glic 的 crt

`ld -o test -dynamic-linker /lib64/ld-linux-x86-64.so.2 /usr/lib/x86_64-linux-gnu/crt1.o /usr/lib/x86_64-linux-gnu/crti.o -lc test.o /usr/lib/x86_64-linux-gnu/crtn.o`

调用 `link.sh test.o test`

## DEMO
 ![image](https://github.com/Mithrilwoodrat/naivecompiler/blob/master/demo/demo.gif)

## TODO
 - [x] support extern function decl
 - [x] formatted AST show function
 - [x] Implement Expr Class for Gen different Code in CodeGen 
 * [x] support StringLiteral in backend 
   - NodeFactory CreateValueNode return different Node Class
 * support array and pointer in backend
 - [] support void type in funcdecl
 - [] support empty return stmt
 - [x] support '||' '&&' binaryOp (frontend and backend)
 - [x] refact condition generate
 - [x] Read Clang CFG.cpp and refact ASTRewrite Class
