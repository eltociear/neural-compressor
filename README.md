<div align="center">
  
Intel® Neural Compressor
===========================
<h3> An open-source Python library supporting popular model compression techniques on all mainstream deep learning frameworks (TensorFlow, PyTorch, ONNX Runtime, and MXNet)</h3>

[![python](https://img.shields.io/badge/python-3.7%2B-blue)](https://github.com/intel/neural-compressor)
[![version](https://img.shields.io/badge/release-1.14-green)](https://github.com/intel/neural-compressor/releases)
[![license](https://img.shields.io/badge/license-Apache%202-blue)](https://github.com/intel/neural-compressor/blob/master/LICENSE)
[![coverage](https://img.shields.io/badge/coverage-90%25-green)](https://github.com/intel/neural-compressor)
[![Downloads](https://static.pepy.tech/personalized-badge/neural-compressor?period=total&units=international_system&left_color=grey&right_color=green&left_text=downloads)](https://pepy.tech/project/neural-compressor)
</div>

---
<div align="left">

Intel® Neural Compressor, formerly known as Intel® Low Precision Optimization Tool, is an open-source Python library that runs on Intel CPUs and GPUs, which delivers unified interfaces across multiple deep-learning frameworks for popular network compression technologies such as quantization, pruning, and knowledge distillation. This tool supports automatic accuracy-driven tuning strategies to help the user quickly find out the best quantized model. It also implements different weight-pruning algorithms to generate a pruned model with predefined sparsity goal. It also supports knowledge distillation to distill the knowledge from the teacher model to the student model. 
Intel® Neural Compressor is a critical AI software component in the [Intel® oneAPI AI Analytics Toolkit](https://software.intel.com/content/www/us/en/develop/tools/oneapi/ai-analytics-toolkit.html).


**Visit the Intel® Neural Compressor online document website at: <https://intel.github.io/neural-compressor>.**   

## Installation

### Prerequisites

Python version: 3.7, 3.8, 3.9, 3.10

### Install on Linux
- Release binary install 
  ```Shell
  # install stable basic version from pypi
  pip install neural-compressor
  # or install stable full version from pypi (including GUI)
  pip install neural-compressor-full
  ```
- Nightly binary install
  ```Shell
  git clone https://github.com/intel/neural-compressor.git
  cd neural-compressor
  pip install -r requirements.txt
  # install nightly basic version from pypi
  pip install -i https://test.pypi.org/simple/ neural-compressor
  # or install nightly full version from pypi (including GUI)
  pip install -i https://test.pypi.org/simple/ neural-compressor-full
  ```
More installation methods can be found at [Installation Guide](./docs/source/installation_guide.md). Please check out our [FAQ](./docs/source/faq.md) for more details.

## Getting Started
### Quantization with Python API    

```shell
# A TensorFlow Example
pip install tensorflow
# Prepare fp32 model
wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_6/mobilenet_v1_1.0_224_frozen.pb
```
```python
from neural_compressor.config import PostTrainingQuantConfig
from neural_compressor.data.dataloaders.dataloader import DataLoader
from neural_compressor.data import Datasets

dataset = Datasets('tensorflow')['dummy'](shape=(1, 224, 224, 3))
from neural_compressor.quantization import fit
config = PostTrainingQuantConfig()
fit(
  model="./mobilenet_v1_1.0_224_frozen.pb",
  conf=config,
  calib_dataloader=DataLoader(framework='tensorflow', dataset=dataset),
  eval_dataloader=DataLoader(framework='tensorflow', dataset=dataset))
```
### Quantization with [JupyterLab Extension](./neural_coder/extensions/neural_compressor_ext_lab/README.md)
Search for ```jupyter-lab-neural-compressor``` in the Extension Manager in JupyterLab and install with one click:

<a target="_blank" href="./neural_coder/extensions/screenshots/extmanager.png">
  <img src="./neural_coder/extensions/screenshots/extmanager.png" alt="Extension" width="35%" height="35%">
</a>
  
### Quantization with [GUI](./docs/source/bench.md)
```shell
# An ONNX Example
pip install onnx==1.12.0 onnxruntime==1.12.1 onnxruntime-extensions
# Prepare fp32 model
wget https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet50-v1-12.onnx
# Start GUI
inc_bench
```
<a target="_blank" href="./docs/source/_static/imgs/INC_GUI.gif">
  <img src="./docs/source/_static/imgs/INC_GUI.gif" alt="Architecture">
</a>

## System Requirements

### Validated Hardware Environment
#### Intel® Neural Compressor supports CPUs based on [Intel 64 architecture or compatible processors](https://en.wikipedia.org/wiki/X86-64):

* Intel Xeon Scalable processor (formerly Skylake, Cascade Lake, Cooper Lake, and Icelake)
* Future Intel Xeon Scalable processor (code name Sapphire Rapids)

#### Intel® Neural Compressor supports GPUs built on Intel's Xe architecture:

* [Intel® Data Center GPU Flex Series](https://www.intel.com/content/www/us/en/products/docs/discrete-gpus/data-center-gpu/flex-series/overview.html)

#### Intel® Neural Compressor quantized ONNX models support multiple hardware vendors through ONNX Runtime:

* Intel CPU, AMD/ARM CPU, and NVidia GPU. Please refer to the validated model [list](./docs/source/validated_model_list.md#Validated-ONNX-QDQ-INT8-models-on-multiple-hardware-through-ONNX-Runtime).

### Validated Software Environment

* OS version: CentOS 8.4, Ubuntu 20.04  
* Python version: 3.7, 3.8, 3.9, 3.10  

<table class="docutils">
<thead>
  <tr>
    <th>Framework</th>
    <th>TensorFlow</th>
    <th>Intel TensorFlow</th>
    <th>PyTorch</th>
    <th>Intel® Extension for PyTorch*</th>
    <th>ONNX Runtime</th>
    <th>MXNet</th>
  </tr>
</thead>
<tbody>
  <tr align="center">
    <th>Version</th>
    <td class="tg-7zrl"><a href=https://github.com/tensorflow/tensorflow/tree/v2.10.0>2.10.0</a><br>
    <a href=https://github.com/tensorflow/tensorflow/tree/v2.9.1>2.9.1</a><br>
    <a href=https://github.com/tensorflow/tensorflow/tree/v2.8.2>2.8.2</a><br>
    <td class="tg-7zrl"><a href=https://github.com/Intel-tensorflow/tensorflow/tree/v2.10.0>2.10.0</a><br>
    <a href=https://github.com/Intel-tensorflow/tensorflow/tree/v2.9.1>2.9.1</a><br>
    <a href=https://github.com/Intel-tensorflow/tensorflow/tree/v2.8.0>2.8.0</a><br>
    <td class="tg-7zrl"><a href=https://download.pytorch.org/whl/torch_stable.html>1.12.1+cpu</a><br>
    <a href=https://download.pytorch.org/whl/torch_stable.html>1.11.0+cpu</a><br>
    <a href=https://download.pytorch.org/whl/torch_stable.html>1.10.0+cpu</a></td>
    <td class="tg-7zrl"><a href=https://github.com/intel/intel-extension-for-pytorch/tree/v1.12.0>1.12.0</a><br>
    <a href=https://github.com/intel/intel-extension-for-pytorch/tree/1.11.0>1.11.0</a><br>
    <a href=https://github.com/intel/intel-extension-for-pytorch/tree/v1.10.0>1.10.0</a></td>
    <td class="tg-7zrl"><a href=https://github.com/microsoft/onnxruntime/tree/v1.12.1>1.12.1</a><br>
    <a href=https://github.com/microsoft/onnxruntime/tree/v1.11.0>1.11.0</a><br>
    <a href=https://github.com/microsoft/onnxruntime/tree/v1.10.0>1.10.0</a></td>
    <td class="tg-7zrl"><a href=https://github.com/apache/incubator-mxnet/tree/1.8.0>1.8.0</a><br>
    <a href=https://github.com/apache/incubator-mxnet/tree/1.7.0>1.7.0</a><br>
    <a href=https://github.com/apache/incubator-mxnet/tree/1.6.0>1.6.0</a></td>
  </tr>
</tbody>
</table>

> **Note:**
> Set the environment variable ``TF_ENABLE_ONEDNN_OPTS=1`` to enable oneDNN optimizations if you are using TensorFlow v2.6 to v2.8. oneDNN is the default for TensorFlow v2.9.

### Validated Models
Intel® Neural Compressor validated 420+ [examples](./examples) for quantization with a performance speedup geomean of 2.2x and up to 4.2x on VNNI while minimizing accuracy loss. Over 30 pruning and knowledge distillation samples are also available. More details for validated models are available [here](./docs/source/validated_model_list.md).

<div style = "width: 77%; margin-bottom: 2%;">
  <a target="_blank" href="./docs/source/_static/imgs/release_data.png">
    <img src="./docs/source/_static/imgs/release_data.png" alt="Architecture" width=800 height=500>
  </a>
</div>

## Documentation

<table class="docutils">
  <thead>
  <tr>
    <th colspan="9">Overview</th>
  </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="3" align="center"><a href="./docs/source/design.md">Architecture</a></td>
      <td colspan="2" align="center"><a href="https://github.com/intel/neural-compressor/tree/master/examples">Examples</a></td>
      <td colspan="2" align="center"><a href="./docs/source/bench.md">GUI</a></td>
      <td colspan="2" align="center"><a href="https://intel.github.io/neural-compressor/api-documentation/apis.html">APIs</a></td>
    </tr>
    <tr>
      <td colspan="5" align="center"><a href="https://software.intel.com/content/www/us/en/develop/documentation/get-started-with-ai-linux/top.html">Intel oneAPI AI Analytics Toolkit</a></td>
      <td colspan="4" align="center"><a href="https://github.com/oneapi-src/oneAPI-samples/tree/master/AI-and-Analytics">AI and Analytics Samples</a></td>
    </tr>
  </tbody>
  <thead>
  <tr>
    <th colspan="9">Basic API</th>
  </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="2" align="center"><a href="./docs/source/transform.md">Transform</a></td>
      <td colspan="2" align="center"><a href="./docs/source/dataset.md">Dataset</a></td>
      <td colspan="2" align="center"><a href="./docs/source/metric.md">Metric</a></td>
      <td colspan="3" align="center"><a href="./docs/source/objective.md">Objective</a></td>
    </tr>
  </tbody>
  <thead>
    <tr>
      <th colspan="9">Deep Dive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td colspan="2" align="center"><a href="./docs/source/quantization.md">Quantization</a></td>
        <td colspan="1" align="center"><a href="./docs/source/pruning.md">Pruning(Sparsity)</a></td> 
        <td colspan="2" align="center"><a href="./docs/source/distillation.md">Knowledge Distillation</a></td>
        <td colspan="2" align="center"><a href="./docs/source/mixed_precision.md">Mixed Precision</a></td>
        <td colspan="2" align="center"><a href="./docs/source/orchestration.md">Orchestration</a></td>
    </tr>
    <tr>
        <td colspan="2" align="center"><a href="./docs/source/benchmark.md">Benchmarking</a></td>
        <td colspan="3" align="center"><a href="./docs/source/distributed.md">Distributed Training</a></td>
        <td colspan="2" align="center"><a href="./docs/source/tensorboard.md">TensorBoard</a></td>
    </tr>
    <tr>
        <td colspan="4" align="center"><a href="./docs/source/distillation_quantization.md">Distillation for Quantization</a></td>
        <td colspan="5" align="center"><a href="https://github.com/intel/neural-compressor/tree/master/neural_coder">Neural Coder</a></td>
    </tr>    
    
  </tbody>
  <thead>
      <tr>
        <th colspan="9">Advanced Topics</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td colspan="6" align="center"><a href="./docs/source/adaptor.md">Adaptor</a></td>
          <td colspan="6" align="center"><a href="./docs/source/tuning_strategies.md">Strategy</a></td>
      </tr>
  </tbody>
</table>

## Selected Publications/Events
* [#MLefficiency — Optimizing transformer models for efficiency](https://medium.com/@kawapanion/mlefficiency-optimizing-transformer-models-for-efficiency-a9e230cff051)(Dec 2022)
* [One-Click Acceleration of Hugging Face Transformers with Intel’s Neural Coder](https://medium.com/intel-analytics-software/one-click-acceleration-of-huggingface-transformers-with-optimum-intel-by-neural-coder-f35ca3b1a82f)(Dec 2022)
* [One-Click Quantization of Deep Learning Models with the Neural Coder Extension](https://medium.com/intel-analytics-software/one-click-quantize-your-deep-learning-code-in-visual-studio-code-with-neural-coder-extension-8be1a0022c29)(Dec 2022)
* [Accelerate Stable Diffusion with Intel Neural Compressor](https://medium.com/intel-analytics-software/accelerating-stable-diffusion-inference-through-8-bit-post-training-quantization-with-intel-neural-e28f3615f77c)(Dec 2022)
* [Intel together with Tencent deepens the cooperation to build a cloud foundation for digital and intelligent industry](https://mp.weixin.qq.com/s/CPz9-5Nsh-5N9Q8-UmK--w) (Dec 2022)
* [Running Fast Transformers on CPUs: Intel Approach Achieves Significant Speed Ups and SOTA Performance](https://medium.com/syncedreview/running-fast-transformers-on-cpus-intel-approach-achieves-significant-speed-ups-and-sota-448521704c5e) (Nov 2022)

> View our [full publication list](./docs/source/publication_list.md).

## Additional Content

* [Release Information](./docs/source/releases_info.md)
* [Contribution Guidelines](./docs/source/CONTRIBUTING.md)
* [Legal Information](./docs/source/legal_information.md)
* [Security Policy](SECURITY.md)
* [Intel® Neural Compressor Website](https://intel.github.io/neural-compressor)

## Hiring

We are actively hiring. Send your resume to inc.maintainers@intel.com if you are interested in model compression techniques.
