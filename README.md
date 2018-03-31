## 使用方法

使用 `python2 compiler.py <input>` 显示 AST

使用 `python2 compiler.py <input> <output>` 生成 obj

使用 `ld -e <symbol>` 将 obj 文件 链接为 ELF， 并指定 <symbol> 为 entry point。（由于未给 naivecompiler 实现 crt， entry point 的函数不能返回参数，只能设置为 void）
