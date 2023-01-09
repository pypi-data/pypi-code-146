import time

from model import Model
from model_composition import ModelComposition
from utils import preprocess

from servicefoundry.function_service import BuildConfig, FunctionService, remote

# composed_model = ModelComposition(model_1_path="foo", model_2_path="bar", model_3_path="baz")
composed_model = remote(
    ModelComposition,
    init_kwargs=dict(model_1_path="foo", model_2_path="bar", model_3_path="baz"),
)


preprocess_service = FunctionService(
    name="preprocess-service",
    build_config=BuildConfig(pip_packages=["numpy<1.22.0"]),
    port=7000,
)

preprocess_service.register_function(preprocess)


model_service = FunctionService(name="model-service", port=7001)


model_1 = remote(
    Model,
    init_kwargs={"model_path": composed_model.init_kwargs["model_1_path"]},
    name="model_1",
)
model_2 = remote(
    Model,
    init_kwargs={"model_path": composed_model.init_kwargs["model_2_path"]},
    name="model_2",
)
model_3 = remote(
    Model,
    init_kwargs={"model_path": composed_model.init_kwargs["model_2_path"]},
    name="model_3",
)
model_service.register_class(model_1)
model_service.register_class(model_2)
model_service.register_class(model_3)


# composed_model = remote(
#     ModelComposition,
#     init_kwargs=dict(model_1=model_1, model_2=model_2, model_3=model_3,),
# )
composed_model_service = FunctionService(name="composed-model-service", port=7002)
composed_model_service.register_class(composed_model)


print(preprocess_service)
print(model_service)
print(composed_model_service)

preprocess_service.run()
model_service.run()
composed_model_service.run()


time.sleep(1)

print(composed_model.predict(image_url="foo"))
time.sleep(1)


# 1.Multiple classes, each class can have its own route prefix.
# # 2.module vs filepath. Can I import a path directly as a module. This is relative to source.
# 3.What is the FQN for a normal function and a method. which I can detirministically generate at run time.
# 4. what if someone uses the same class and wnat to init it with two diff model path.
