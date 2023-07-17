# Development of AI and Robotics Assisted Automated Pavement Crack Evaluation System

This is the source code of the paper titled "Development of AI and Robotics Assisted Automated Pavement Crack Evaluation System". We provide the code of the robot development, deep learning model development code, test code, and the pre-trained model. Along with the computer vision part, this repo also contains the code for impact echo sensors and NI-DAQ card; which is not covered in this article but rather covered in the M.Sc thesis of Md. Al-Masrur Khan (http://dx.doi.org/10.13140/RG.2.2.15424.10243)

Khan, M.A.-M.; Harseno, R.W.; Kee, S.-H.; Nahid, A.-A. Development of AI- and Robotics-Assisted Automated Pavement-Crack-Evaluation System. Remote Sens. 2023, 15, 3573. https://doi.org/10.3390/rs15143573

# Key Files
1. [Client](https://github.com/Masrur02/AMSEL_robot/tree/version_14.12.2021/Client)- This folder should be in the user end computer which will be used to control the robot.
2. [main.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Client/main.py)- This code inside the Client folder should be run to run the desktop app for controlling the robot. This desktop app can be converted as an executable file also.

3. [Server](https://github.com/Masrur02/AMSEL_robot/tree/version_14.12.2021/Server)-This folder should be in the mini pc of the robot to execute the command from the user.
4. [server.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Server/server.py)- This code inside the Server folder should be run to make the robot function.
# Supplementary Files
5. [RCDNet.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/RCDNet.ipynb) -Assuming you have any crack detection dataset, this is the proposed RCDNet to train using that data.
6. [in.h5](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Server/in.h5)-This is the weighted file for detecting cracks in any indoor environment. This weighted file works better for an indoor environment.
7. [out.h5](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Server/out.h5)-This is the weighted file for detecting cracks in any outdoor environment. This weighted file works better for outdoor environments.
8. [Detection.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Detection.py)- Using the trained model and an input video, this predicts the cracks and returns the original video with predicted cracks onto it. This code is implemented inside the robot by using the weighted file for detecting the cracks using the images captured by the camera installed in the robot. However, this file can be also used outside the robotic vehicle for detecting cracks from any input video.
9. [Measurement_new.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Measurement_new.py)-Assuming you have predicted black and white images, this code can be used for measuring the crack's length, width, area.
10. [stiching.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Stitching.py)-Assuming you have the predicted images from a grid, you can stitch the images based on grid position by this code.
11. [Ni_sensors.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/NI_sensor.py)-This is the Python code for the NI-DAQ device.

# App for Controlling the Robot
![gui](https://github.com/Masrur02/AMSEL_robot/assets/33350185/70617a74-a590-46ba-8d60-47b1a5306399)
# Developed Robot
![a](https://github.com/Masrur02/AMSEL_robot/assets/33350185/62a16a8d-030c-48c9-8663-dc443e0ffd0d)


# RCDNet Architecture
![Screenshot_2023-06-11_01-12-15](https://github.com/Masrur02/AMSEL_robot/assets/33350185/2a838675-e453-44cf-b912-95281c01e742)

# Some Results
![a](https://github.com/Masrur02/AMSEL_robot/assets/33350185/a1381022-3e19-49ee-87b4-b1fb2365cd4e)
![b](https://github.com/Masrur02/AMSEL_robot/assets/33350185/e30a7d67-74ff-4e1b-9307-25eeca688813)
![c](https://github.com/Masrur02/AMSEL_robot/assets/33350185/d3993053-eb63-4d8c-87ae-d09c48a84f60)
![d](https://github.com/Masrur02/AMSEL_robot/assets/33350185/1e78f8b1-583f-4937-bfb5-697659089d66)
![image](https://github.com/Masrur02/AMSEL_robot/assets/33350185/e750d66b-343e-4487-bf59-b55319c635a0)

# Citation
Please cite our paper if you use this code or the mixed dataset in your own work:
@article{remotesensing-2465244,
  title={Development of AI- and Robotics-Assisted Automated Pavement-Crack-Evaluation System},
  author={Khan, M.A.-M.; Harseno, R.W.; Kee, S.-H.; Nahid, A.-A.},
  journal={Remote Sensing},
  volume={15},
  year={2023},
}









