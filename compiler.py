# -*- coding: utf-8 -*-
from llvmlite import ir
import llvmlite.binding as llvm

# Create some useful types
Int32 = ir.IntType(32)
main_func = ir.FunctionType(Int32, ())

# Create an empty module...
module = ir.Module(name=__file__)
# and declare a function named "fpadd" inside it
main = ir.Function(module, main_func, name="main")

# Now implement the function
block = main.append_basic_block(name="entry")
builder = ir.IRBuilder(block)
a, b = ir.Constant(Int32, 1), ir.Constant(Int32, 2)
result = builder.add(a, b, name="res")
builder.ret(result)

# Print the module IR
print(module)

def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_triple(u'x86-64')
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    return mod


engine = create_execution_engine()
# module.verify()
# engine.add_module(module)
# engine.finalize_object()
# func_ptr = engine.get_function_address("main")
# # Run the function via ctypes
# cfunc = CFUNCTYPE(c_int)(func_ptr)
# res = cfunc()
# print("ret=", res)

