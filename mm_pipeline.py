from kfp import compiler
from kfp.dsl import container_component, component
from kfp.dsl import ContainerSpec
from kfp.dsl import Dataset
from kfp.dsl import Input
from kfp.dsl import Output
from kfp.dsl import pipeline


@component
def component1(text: str, output_gcs: Output[Dataset]):
    with open(output_gcs.path, 'w') as f:
        f.write(text)


@component
def component2(input_gcs: Input[Dataset]):
    with open(input_gcs.path, 'r') as f:
        lines = f.readlines()
        print(lines)


@pipeline(name='mm_pipeline')
def mm_pipeline():
    component_1 = component1(text='hello world Matteo')
    component_2 = component2(input_gcs=component_1.outputs['output_gcs'])


if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=mm_pipeline,
        package_path='mm_pipeline.yaml')