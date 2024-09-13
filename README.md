# Yoodle
A Buildings Doodle Classifier!!

**Yes, added a dropdown to select a building, merely for data collection for the AI**. Model will learn if image is different from selected, thus getting better and better
Working on the deployment!!


![How it works](https://github.com/Ahmad-Waseem/Yoodle/blob/1fbbc2a3c058155dc22e3b913736630e0f1c1928/Yoodle-AIBuildings.gif)






## Data Prep : Create Doodle like Dataset
** *Find Code/DataPrep.ipynb for giving raw dataset; It will convert any image to doodle-like
There are around 32 Classes of famous buildings in raw dataset DataPrep.ipynb expands them to x6, and the data-cleanup in Yoodle.ipynb clears all the files with untrainable or courrupt files It is advised to Augment the data before training for better results!* **

This was a lot helpful in Dataset Creation:
    - https://subscription.packtpub.com/book/data/9781788396905/1/ch01lvl1sec19/image-warping
