from argparse import ArgumentParser
from neural_compressor.data.datasets.dataset import TensorflowImageRecord
from neural_compressor.data.transforms.imagenet_transform import BilinearImagenetTransform
from neural_compressor.data.transforms.transform import ComposeTransform
from neural_compressor.data.dataloaders.default_dataloader import DefaultDataLoader
from neural_compressor.config import PostTrainingQuantConfig
from neural_compressor.config import BenchmarkConfig

def main():
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

    if args.tune:
        from neural_compressor.quantization import fit
        config = PostTrainingQuantConfig(calibration_sampling_size=[20])
        q_model = fit(
            model="./mobilenet_v1_1.0_224_frozen.pb",
            conf=config,
            calib_dataloader=calib_dataloader,
            eval_dataloader=eval_dataloader)
        q_model.save('./int8.pb')

    if args.benchmark:
        from neural_compressor.benchmark import fit
        conf = BenchmarkConfig(iteration=100, cores_per_instance=4, num_of_instance=7)
        fit(model='./int8.pb', config=conf, b_dataloader=eval_dataloader)

if __name__ == "__main__":
    main()
