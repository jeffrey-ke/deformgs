import argparse
import os 
import glob
import natsort
import shutil 

parser = argparse.ArgumentParser()

parser.add_argument('--results',type=str,default="/data/bart/CVPR_2024/final_results/")
parser.add_argument('--output',type=str,default="/data/bart/4DGaussians/output/final_scenes/")

parser.add_argument('--test_path',type=str,default="test/ours_30000")
parser.add_argument("--executable",type=str,default="/data/bart/4DGaussians/scripts/align_eval_trajs.py")
args = parser.parse_args()

output_dirs = natsort.natsorted(glob.glob(os.path.join(args.output,"**")))
# filter out non directories
output_dirs = [x for x in output_dirs if os.path.isdir(x)]
scenes = [x.split("/")[-1] for x in output_dirs]

output_dirs = [os.path.join(x,args.test_path) for x in output_dirs]
trajs_paths = [os.path.join(x,"all_trajs.npz") for x in output_dirs]

results_dirs = [os.path.join(args.results,scene) for scene in scenes]
gt_paths = [os.path.join(x,"gt.npz") for x in results_dirs]

for gt_path, traj_path, results_dir in zip(gt_paths,trajs_paths, results_dirs):
    print("gt_path: {}".format(gt_path))
    print("traj_path: {}".format(traj_path))
    
    command = "python3 {} --gt_file {} --traj_file {}".format(args.executable,gt_path,traj_path)
    
    # execute command
    os.system(command)
    
    output_dir = os.path.join(results_dir,"ours")
    # delete the output dir if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    source_file = traj_path.replace(".npz","_aligned.npz")
    output_file = os.path.join(output_dir,"traj.npz")
    
    print("Copying the output")
    # copy the aligned traj to the output dir
    shutil.copyfile(source_file,output_file)