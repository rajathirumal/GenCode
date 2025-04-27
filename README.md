# <span style="color: #0080FF;"> GenCode - AI </span>
This is a template for your model that can do autocomplete on your code. This is targeted to the Python programming language.

It is a basic implementation of the series [Generative Python transformer](https://www.youtube.com/watch?v=3P3TcKaegbA&list=PLQVvvaa0QuDdKvPge9PXQtFzvhMRyFPhW) from <img src="https://yt3.googleusercontent.com/ytc/AGIKgqPYFBC1JDRcLeC0R6fkKICvCVeCEpuiyUr78MeUkA=s176-c-k-c0x00ffffff-no-rj" alt="Channel Profile Picture" style="width:15px;height:15px;"> [Sendex](https://www.youtube.com/@sentdex) 


# Dataset 
Dataset used is purly python code extracted from GitHub.

The test was performed with the below parameters, the parameters could be changed as per your hardware.

We have tried our best to pick some good repos from GitHub. 
 - Repos with `stars > 20` have been picked for the dataset preparation
 - Repos created on and after `01 May 2023` and on and before `30 June 2023`
 - Target language `Python`

To test this code I have used Macbook M2 Pro.

| Hardware | Specification |
| ------------- | ------------- |
| Chip set      | Apple silion M2  |
| Memory        | 16 GB  |
| CPU           | 10 core  |
| GPU           | 16 core  |
| ANE           | 16 core|

Training models on the Apple Neural Engine (ANE) is not supported in PyTorch and therefore not used. We have utilized the GPU with MPS. Refer to "[Accelerated PyTorch training on Mac](https://developer.apple.com/metal/pytorch/)" for more details.