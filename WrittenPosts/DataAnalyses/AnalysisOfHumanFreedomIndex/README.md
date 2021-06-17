# This Folder Contains Data Analysis and Code

This folder contains the unfiltered code and data analysis. I recommend only looking over this folder if you 
wish to understand, view, or critique (would love that) the analysis completed. Otherwise, if you wish to view 
the more...comprehendable conclusion and insights, return to the directory above [here](https://github.com/amm414/Projects/tree/master/WrittenPosts/DataAnalyses).

# Analysis of the Human Freedom Index 

This is the Repo for the Analysis of Cato Institute's Human Freedom Index.

Details of the Report published anually (We are using the 2016 version), can be found at: 

https://www.cato.org/human-freedom-index-new

Dataset Aquired at Kaggle:

https://www.kaggle.com/gsutters/the-human-freedom-index

# Inside the Repo:

The RMarkdown files, R scripts, knitted PDFs, and the dataset itself are located in this directory. 
In order to run the script, the user must correctly identify the correct path that the dataset is on the hard drive. 
The proper libraries must be installed, and errors will be thrown if they are not installed.

The Libraries Used are:
gbm, calibrate, gam, boot, splines, dplyr, ggplot2, FNN, glmnet, pls, MASS, leaps, 
tree, rpart.plot, randomForest, reshape2

The Script named "Install_Library_Script.R" will install all the libraries listed here. 
All libraries on the computer will be updated and overwritten by this script if they do exist.

## Specific Files

### The Main File: *Documentation_of_Code_Appendix_4.4.19.Rmd* and the corresponding *PDF*:
  - This contains all the different methods in one great place. 
  - Though, does not include the:
    - script for creating the graph of the permutation test results and correlation between all features
    - script comparing the different datasets (2008, 2016, no outliers/influential observations, and all data)
    
#### The Secondary File: *Running_Multiple_Tests_Linear_Models.Rmd* and corresponding *PDF*
  - This file analyzes whether removing outliers/influential observations effect results and the average models
  - analyzes whether the first year the dataset contains (2008) is different from (2016)

#### Miscellaneous Scripts:
  - Install_Libraries_Script.R: installes or updates all neccesary libraries.
  - Permutation_Testing_and_Correlation_Plot.R: Allows user to view visual plot of the correlations and 
  whether the results are significant using a permutation test 
  - Permutation_Testing_and_Correlation_Heat_Map.png with just the graph of the Correlation and Permutation Testing Plots if one wishes to not run it. 
