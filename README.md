# Copernicus_Project

# Overviewpyt

# Requirements

The following packages are required:
* numpy (ver. 1.18.1)
* pandas (ver. 1.0.1)
* scikit-learn (ver. 0.22.1)
* pyquaternion (ver. 0.9.5)
* matplotlib (ver. 3.1.3)
* opencv-python (ver. 4.2.0.32)
* keras (ver. 2.3.1)
* tensorflow-gpu (ver. 2.1.0)
* scikit-image (ver. 0.16.2)
* xlrd (ver. 1.2.0)
* Quaternion (ver. 0.3.1)

# Datasets

## Pre-processing the datasets

The folder for each dataset in this repo (David_MMSys_18, FAN_NOSSDAV_17, Nguyen_MM_18, Xu_CVPR_18, Xu_PAMI_18) contains a file called "Reading_Dataset.py", this file can be used to read and process the original dataset.

#### Reproduce Table of Comparison with NOSSDAV17

**Requirements**:
You must download the files:
   - ```./Fan_NOSSDAV_17/dataset/sensory/tile_replica``` from https://unice-my.sharepoint.com/:f:/g/personal/lucile_sassatelli_unice_fr/EqCSPdafbiNNrlmDOcqNSKQBHWLl7Ol26rreKDti6w7W-A?e=Oh2GGJ
   - For pos_only baseline: ```./Fan_NOSSDAV_17/pos_only/Models_EncDec_eulerian_init_5_in_5_out_25_end_25/weights.hdf5``` from https://unice-my.sharepoint.com/:f:/g/personal/lucile_sassatelli_unice_fr/EqCSPdafbiNNrlmDOcqNSKQBHWLl7Ol26rreKDti6w7W-A?e=Oh2GGJ
   - For TRACK: ```./Fan_NOSSDAV_17/TRACK/Models_EncDec_3DCoords_ContSal_init_5_in_5_out_25_end_25/weights.hdf5``` from https://unice-my.sharepoint.com/:f:/g/personal/lucile_sassatelli_unice_fr/EqCSPdafbiNNrlmDOcqNSKQBHWLl7Ol26rreKDti6w7W-A?e=Oh2GGJ
   - For TRACK: ```./Fan_NOSSDAV_17/extract_saliency``` from https://unice-my.sharepoint.com/:f:/g/personal/lucile_sassatelli_unice_fr/EqCSPdafbiNNrlmDOcqNSKQBHWLl7Ol26rreKDti6w7W-A?e=Oh2GGJ
   
Or run the commands: 
   - ```python ./Fan_NOSSDAV_17/Read_Dataset.py -create_tile_replica```
   - For pos_only baseline: ```python training_procedure.py -train -gpu_id 0 -dataset_name Fan_NOSSDAV_17 -model_name pos_only -m_window 5 -h_window 25 -provided_videos```
   - For TRACK: ```python ./Fan_NOSSDAV_17/Read_Dataset.py -creat_cb_sal -provided_videos```

| Method | Accuracy | F-Score | Rank Loss |
| --- | --- | --- | --- |
| NOSSDAV17-Tile | 84.22% | 0.53 | 0.19 |
| NOSSDAV17-Orient. | 86.35% | 0.62 | 0.14 |
| No-motion baseline | 95.79% | 0.87 | 0.10 |
| Position-only baseline | 96.30% | 0.89 | 0.09 |
| TRACK-CBSal | 95.48% | 0.85 | 0.15 |

To reproduce the Table above: Comparison with NOSSDAV17: Performance of Tile- and Orientation-based networks of NOSSDAV17 compared against our position-only baseline.
You can run the script under ```"Fan_NOSSDAV_17/Baselines.py"```.

To get the results for:

*  **"No-motion baseline"**: Run the script with the following options:
```
python ./Fan_NOSSDAV_17/Baselines.py -gpu_id "" -model_name no_motion
```

*  **"Pos-only baseline"**: Run the script with the following options:
```
python ./Fan_NOSSDAV_17/Baselines.py -gpu_id 0 -model_name pos_only
```

*  **"TRACK"**: Run the script with the following options:
```
python ./Fan_NOSSDAV_17/Baselines.py -gpu_id 0 -model_name TRACK
```

