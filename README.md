# Development of AI and Robotics Assisted Automated Pavement Crack Evaluation System

This is the source code of Development of AI and Robotics Assisted Automated Pavement Crack Evaluation System. We provide the code of the robot development, deep learning model development code, test code and the pretrained model. Along with the computer vision part, this repo also contains the code for impact echo sensors and NI-DAQ card; which is not covered in this article.

# Key Files
1. [Client](https://github.com/Masrur02/AMSEL_robot/tree/version_14.12.2021/Client)- This folder should be in the user end computer which will be used to control the robot.
2. [main.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Client/main.py)- This code inside the Client folder should be run to run the desktop app for controlling the robot. This desktop app can be converted as an executable file also.

3. [Server](https://github.com/Masrur02/AMSEL_robot/tree/version_14.12.2021/Server)-This folder should be in the mini pc of robot to executing the command from the user.
4. [server.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Server/server.py)- This code inside the Server folder should be run to make the robot functioning.
# Supplementary Files
5. [RCDNet.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/RCDNet.ipynb) -Assuming you have any crack detection dataset, this is the proposed RCDNet to train using that data.
6. [in.h5](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Server/in.h5)-This is the weighted file for detecting cracks in any indoor environment. This weighted file works better for indoor environment.
7. [out.h5](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Server/out.h5)-This is the weighted file for detecting cracks in any outdoor environment. This weighted file works better for outdoor environment.
8. [Detection.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Detection.py)- Using the trained model and an input video, this predicts the cracks, and returns the original video with predicted cracks onto it. This code is implemented inside the robot by using the weighted file for detecting the cracks using the images captured by the camera installed in the robot. However, this file can be also used outside the robotic vehicle for detecting cracks from any input video.
9. [Measurement_new.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Measurement_new.py)-Assuming you have predicted black and white images, this code can be used for measuring the crack's length, width, area.
10. [stiching.py](https://github.com/Masrur02/AMSEL_robot/blob/version_14.12.2021/Stitching.py)-Assuming you have the predicted images from a grid, you can stiched the images based on grid position by this code.

# App for Controlling the Robot
![gui](https://github.com/Masrur02/AMSEL_robot/assets/33350185/70617a74-a590-46ba-8d60-47b1a5306399)

# RCDNet Architecture
![Screenshot_2023-06-11_01-12-15](https://github.com/Masrur02/AMSEL_robot/assets/33350185/2a838675-e453-44cf-b912-95281c01e742)

# Some Results
![a](https://github.com/Masrur02/AMSEL_robot/assets/33350185/a1381022-3e19-49ee-87b4-b1fb2365cd4e)
![b](https://github.com/Masrur02/AMSEL_robot/assets/33350185/e30a7d67-74ff-4e1b-9307-25eeca688813)
![c](https://github.com/Masrur02/AMSEL_robot/assets/33350185/d3993053-eb63-4d8c-87ae-d09c48a84f60)
![d](https://github.com/Masrur02/AMSEL_robot/assets/33350185/1e78f8b1-583f-4937-bfb5-697659089d66)








