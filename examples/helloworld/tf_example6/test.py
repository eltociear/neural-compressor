import tensorflow as tf
from argparse import ArgumentParser
from neural_compressor.metric.metric import TensorflowTopK
from neural_compressor.data.transforms.imagenet_transform import LabelShift
from neural_compressor.data.datasets.dataset import TensorflowImageRecord
from neural_compressor.data.transforms.imagenet_transform import BilinearImagenetTransform
from neural_compressor.data.transforms.transform import ComposeTransform
from neural_compressor.data.dataloaders.default_dataloader import DefaultDataLoader
from neural_compressor.config import PostTrainingQuantConfig, BenchmarkConfig

import numpy as np
import time

arg_parser = ArgumentParser(description='Parse args')
arg_parser.add_argument('--dataset_location',
                        help='location of calibration dataset and evaluate dataset')
arg_parser.add_argument('--benchmark', action='store_true', help='run benchmark')
arg_parser.add_argument('--tune', action='store_true', help='run tuning')
args = arg_parser.parse_args()

calib_dataset = TensorflowImageRecord(root=args.dataset_location, transform= \
        ComposeTransform(transform_list= [BilinearImagenetTransform(height=224, width=224)]))
calib_dataloader = DefaultDataLoader(dataset=calib_dataset, batch_size=10)

eval_dataset = TensorflowImageRecord(root=args.dataset_location, transform=ComposeTransform(transform_list= \
        [BilinearImagenetTransform(height=224, width=224)]))
eval_dataloader = DefaultDataLoader(dataset=eval_dataset, batch_size=1)

def evaluate(model):
    """Custom evaluate function to estimate the accuracy of the model.

    Args:
        model (tf.Graph_def): The input model graph

    Returns:
        accuracy (float): evaluation result, the larger is better.
    """
    input_tensor = model.input_tensor
    output_tensor = model.output_tensor if len(model.output_tensor)>1 else \
                    model.output_tensor[0]
    iteration = -1
    if args.benchmark:
        iteration = 100
    postprocess = LabelShift(label_shift=1)
    metric = TensorflowTopK(k=1)

    def eval_func(dataloader):
        latency_list = []
        for idx, (inputs, labels) in enumerate(dataloader):
            # dataloader should keep the order and len of inputs same with input_tensor
            inputs = np.array([inputs])
            assert len(input_tensor) == len(inputs), \
                'inputs len must equal with input_tensor'
            feed_dict = dict(zip(input_tensor, inputs))

            start = time.time()
            predictions = model.sess.run(output_tensor, feed_dict)
            end = time.time()

            predictions, labels = postprocess((predictions, labels))
            metric.update(predictions, labels)
            latency_list.append(end-start)
            if idx + 1 == iteration:
                break
        latency = np.array(latency_list).mean()
        return latency

    latency = eval_func(eval_dataloader)
    if args.benchmark:
        print("Batch size = 1")
        print("Latency: {:.3f} ms".format(latency * 1000))
        print("Throughput: {:.3f} images/sec".format(1. / latency))
    acc = metric.result()
    return acc

def main():
    if args.tune:
        from neural_compressor.quantization import fit
        config = PostTrainingQuantConfig(calibration_sampling_size=[20])
        quantized_model = fit(
            model="./mobilenet_v1_1.0_224_frozen.pb",
            conf=config,
            calib_dataloader=calib_dataloader,
            eval_dataloader=eval_dataloader)
        tf.io.write_graph(graph_or_graph_def=quantized_model.model,
                          logdir='./',
                          name='int8.pb',
                          as_text=False)

    if args.benchmark:
        from neural_compressor.model.model import Model
        evaluate(Model('./int8.pb'))

if __name__ == "__main__":
    main()
