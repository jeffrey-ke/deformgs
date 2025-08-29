FROM bartduis/4dgausians:latest
RUN echo "conda activate Gaussians4D" >> ~/.bashrc
WORKDIR /workspace
RUN apt-get update
RUN apt-get install -y git
SHELL ["/root/miniconda3/bin/conda", "run", "-n", "Gaussians4D", "bash", "-c"]
ARG TORCH_CUDA_ARCH_LIST="8.6"
RUN pip install git+https://github.com/ingra14m/depth-diff-gaussian-rasterization.git@f2d8fa9921ea9a6cb9ac1c33a34ebd1b11510657
RUN pip install git+https://gitlab.inria.fr/bkerbl/simple-knn.git@44f764299fa305faf6ec5ebd99939e0508331503
RUN pip install h5py open3d seaborn
