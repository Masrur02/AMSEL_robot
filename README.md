# Development of AI and Robotics Assisted Automated Pavement Crack Evaluation System

This is the source code of Development of AI and Robotics Assisted Automated Pavement Crack Evaluation System. We provide the code of the robot development, deep learning model development code, test code and the pretrained model. Along with the computer vision part, this repo also contains the code for impact echo sensors and NI-DAQ card; which is not covered in this article.

# Key Files
1. [LLDNet.ipynb](https://github.com/Masrur02/LLDNet/blob/main/LLDNet.ipynb)- Assuming you have downloaded the training images and labels above, this is the proposed LLDNet to train using that data.

2. [LLDNet.h5](https://github.com/Masrur02/LLDNet/blob/main/LLDNet.h5)-These are the final outputs from the above CNN. Note that if you train the file above the originals here will be overwritten! These get fed into the below.
3. [Lane_detection.py](https://github.com/Masrur02/LLDNet/blob/main/Lane_detection.py) -Using the trained model and an input video, this predicts the lane, and returns the original video with predicted lane lines drawn onto it.


# RCDNet Architecture
![image](https://user-images.githubusercontent.com/33350185/181172871-77060790-4437-44c9-ba26-d88ee953e114.png)

# Some Results
![image](https://user-images.githubusercontent.com/33350185/181173323-d740d99e-29f1-4bad-946c-57e10f17db11.png)
![image](https://user-images.githubusercontent.com/33350185/181174138-31ac678a-080f-44eb-9ad0-2b0dac4efcb7.png)
![image](https://user-images.githubusercontent.com/33350185/181174183-7788e669-e02e-4215-b771-9319c78a31fe.png)



# Key Files
1. [LLDNet.ipynb](https://github.com/Masrur02/LLDNet/blob/main/LLDNet.ipynb)- Assuming you have downloaded the training images and labels above, this is the proposed LLDNet to train using that data.

2. [LLDNet.h5](https://github.com/Masrur02/LLDNet/blob/main/LLDNet.h5)-These are the final outputs from the above CNN. Note that if you train the file above the originals here will be overwritten! These get fed into the below.
3. [Lane_detection.py](https://github.com/Masrur02/LLDNet/blob/main/Lane_detection.py) -Using the trained model and an input video, this predicts the lane, and returns the original video with predicted lane lines drawn onto it.

# Citation
Please cite our paper if you use this code or the mixed dataset in your own work:
@article{sensors-22-05595,
  title={LLDNet: A Lightweight Lane Detection Approach for Autonomous Cars Using Deep Learning},
  author={Khan, M.A.-M.; Haque, M.F.; Hasan, K.R.; Alamjani, S.H.; Baz, M.; Masud, M.; Al-Nahid, A.},
  journal={Sensors},
  volume={22},
  year={2022},
}




