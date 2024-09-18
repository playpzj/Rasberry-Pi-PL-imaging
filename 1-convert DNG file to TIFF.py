import os
import rawpy
import imageio

root_folder = r'' # select the folder containing the raw DNG files from the Raspberry Pi camera

num_success = 0
num_fail = 0

for folder_path, subfolders, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith('.dng'):
            dng_path = os.path.join(folder_path, filename)
            tiff_path = os.path.join(folder_path, filename[:-4] + '.tiff')
            try:
                with rawpy.imread(dng_path) as raw:
                    rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16)
                imageio.imsave(tiff_path, rgb)
                print(f"Converted {dng_path} to {tiff_path}")
                num_success += 1
            except:
                print(f"Failed to convert {dng_path}")
                num_fail += 1

print(f"Done. {num_success} files successfully converted, {num_fail} files failed to convert.")
