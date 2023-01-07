import tempfile

from kfp import compiler
from kfp import dsl


@dsl.component
def addition_component(num1: int, num2: int) -> int:
    return num1 + num2


@dsl.pipeline(name='addition-pipeline')
def my_pipeline(a: int, b: int, c: int = 10):
    add_task_1 = addition_component(num1=a, num2=b)
    add_task_2 = addition_component(num1=add_task_1.output, num2=c)


cmplr = compiler.Compiler()


def test_compile_pipeline():
    _, filepath = tempfile.mkstemp(suffix=".yaml")
    cmplr.compile(my_pipeline, package_path=filepath)
    assert True


def test_compile_component():
    _, filepath = tempfile.mkstemp(suffix=".yaml")
    cmplr.compile(
        addition_component,
        package_path=filepath,
    )
    assert True
