#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
import numpy as np
from neural_compressor import data
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

flags = tf.compat.v1.flags
FLAGS = flags.FLAGS

## Required parameters
flags.DEFINE_string(
	'input_model', None, 'Run inference with specified keras model.')

flags.DEFINE_string(
	'output_model', None, 'The output quantized model.')

flags.DEFINE_string(
	'mode', 'performance', 'define benchmark mode for accuracy or performance')

flags.DEFINE_bool(
	'tune', False, 'whether to tune the model')

flags.DEFINE_bool(
	'benchmark', False, 'whether to benchmark the model')

flags.DEFINE_string(
	'calib_data', None, 'location of calibration dataset')

flags.DEFINE_string(
	'eval_data', None, 'location of evaluate dataset')

flags.DEFINE_integer(
    'batch_size', 32, 'batch_size of evaluation')

flags.DEFINE_integer(
    'iters', 100, 'maximum iteration when evaluating performance')

from neural_compressor.metric.metric import TensorflowTopK
from neural_compressor.data.datasets.dataset import TensorflowImageRecord
from neural_compressor.data.dataloaders.default_dataloader import DefaultDataLoader
from neural_compressor.data.transforms.transform import ComposeTransform
from neural_compressor.data.transforms.imagenet_transform import LabelShift
from neural_compressor.data.transforms.imagenet_transform import BilinearImagenetTransform

eval_dataset = TensorflowImageRecord(root=FLAGS.eval_data, transform=ComposeTransform(transform_list= \
							[BilinearImagenetTransform(height=224, width=224)]))
if FLAGS.benchmark and FLAGS.mode == 'performance':
	eval_dataloader = DefaultDataLoader(dataset=eval_dataset, batch_size=1)
else:
	eval_dataloader = DefaultDataLoader(dataset=eval_dataset, batch_size=FLAGS.batch_size)
if FLAGS.calib_data:
	calib_dataset = TensorflowImageRecord(root=FLAGS.calib_data, transform=ComposeTransform(transform_list= \
								[BilinearImagenetTransform(height=224, width=224)]))
	calib_dataloader = DefaultDataLoader(dataset=calib_dataset, batch_size=10)

def evaluate(model):
    """Custom evaluate function to inference the model for specified metric on validation dataset.

    Args:
        model (tf.saved_model.load): The input model will be the class of tf.saved_model.load(quantized_model_path).
        
    Returns:
        accuracy (float): evaluation result, the larger is better.
    """
    infer = model.signatures["serving_default"]
    output_dict_keys = infer.structured_outputs.keys()
    output_name = list(output_dict_keys )[0]
    postprocess = LabelShift(label_shift=1)
    metric = TensorflowTopK(k=1)

    def eval_func(dataloader, metric):
        warmup = 5
        iteration = None
        latency_list = []
        if FLAGS.benchmark and FLAGS.mode == 'performance':
            iteration = FLAGS.iters
        for idx, (inputs, labels) in enumerate(dataloader):
            inputs = np.array(inputs)
            input_tensor = tf.constant(inputs)
            start = time.time()
            predictions = infer(input_tensor)[output_name]
            end = time.time()
            predictions = predictions.numpy()
            predictions, labels = postprocess((predictions, labels))
            metric.update(predictions, labels)
            latency_list.append(end - start)
            if iteration and idx >= iteration:
                break
        latency = np.array(latency_list[warmup:]).mean() / eval_dataloader.batch_size
        return latency

    latency = eval_func(eval_dataloader, metric)
    if FLAGS.benchmark and FLAGS.mode == 'performance':
        print("Batch size = {}".format(eval_dataloader.batch_size))
        print("Latency: {:.3f} ms".format(latency * 1000))
        print("Throughput: {:.3f} images/sec".format(1. / latency))
    acc = metric.result()
    return acc

def main(_):
	if FLAGS.tune:
		from neural_compressor import quantization
		from neural_compressor.config import PostTrainingQuantConfig
		op_name_list={
			'StatefulPartitionedCall/mobilenetv2_1.00_224/expanded_conv_depthwise/depthwise':
						{
						'activation':  {'dtype': ['fp32']},
						'weight': {'dtype': ['fp32']},
						},
			'StatefulPartitionedCall/mobilenetv2_1.00_224/expanded_conv_project_BN/FusedBatchNormV3/Mul':
						{
						'activation':  {'dtype': ['fp32']},
						'weight': {'dtype': ['fp32']},
						}										
					}
		conf = PostTrainingQuantConfig(calibration_sampling_size=[20, 50],
										op_name_list=op_name_list)
		q_model = quantization.fit(FLAGS.input_model, conf=conf, calib_dataloader=calib_dataloader,
					eval_func=evaluate)
		q_model.save(FLAGS.output_model)

	if FLAGS.benchmark:
		from neural_compressor.benchmark import fit
		from neural_compressor.config import BenchmarkConfig
		if FLAGS.mode == 'performance':
			conf = BenchmarkConfig(cores_per_instance=4, num_of_instance=7)
			fit(FLAGS.input_model, conf, b_func=evaluate)
		else:
			from neural_compressor.model.model import Model
			model = Model(FLAGS.input_model).model
			accuracy = evaluate(model)
			print('Batch size = %d' % FLAGS.batch_size)
			print("Accuracy: %.5f" % accuracy)

if __name__ == "__main__":
	tf.compat.v1.app.run()
