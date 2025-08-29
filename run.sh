docker run -it \
    --gpus all \
    --rm \
    --network=host \
    --shm-size=50G \
    --name deformgs \
    -v .:/workspace \
    -v ~/data/deformgs/:/workspace/data \
    jeff/deformgs

