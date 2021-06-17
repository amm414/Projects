library(dplyr)
library(reshape2)
library(ggplot2)
library(FNN)
library(boot)
library(glmnet)
library(pls)
library(MASS)
library(leaps)

set.seed(1)
human.freedom.index = read.csv(file ="C:/GitHub/Private-Projects/School/2019-Spring/STAT - Statistical Learning and Data Science/Project/Actual project/the-human-freedom-index/hfi_cc_2018.csv")

cols_to_remove = c("pf_rol", "pf_ss", "pf_movement", "pf_ss_women", "pf_religion", 
                   "pf_association", "pf_expression", "pf_identity", "pf_score", "pf_rank",
                   "ef_government", "ef_legal", "ef_money", "ef_trade", "ef_regulation", 
                   "ef_score", "ef_rank", "pf_identity_sex", "ef_trade_movement", 
                   "pf_ss_disappearances", "ef_regulation_labor", "ef_regulation_business")
human.freedom.index = human.freedom.index %>% dplyr::select(-cols_to_remove)

### Now need to remove columns because TOO many N/A's

cols.to.drop2 = list()    # will create list of column names to drop from dataset
list_counter = 1          # index for the list() object
for (i in 1:ncol(human.freedom.index)){
# checking if the number of N/A's is 100 or more
#     (seemed good with preliminary inspection)
if(sum(is.na(human.freedom.index[,i])) >= 100 ){
  # append the column name that has 100+ N/A's 
  cols.to.drop2[[list_counter]] = colnames(human.freedom.index[i])
  list_counter = list_counter + 1     # update the counter
}
}
# now to 'vectorize' the list by unlist()-ing
cols.to.drop2 = unlist(cols.to.drop2)
ncol(human.freedom.index)   # number of features BEFORE dropping
human.freedom.index = human.freedom.index %>%
  dplyr::select(-cols.to.drop2) 
ncol(human.freedom.index)   # number of features AFTER dropping

nrow(human.freedom.index)   # number of rows BEFORE dropping 
# drop rows with ANY N/A's (this will bias the dataset)
human.freedom.index = human.freedom.index %>% na.omit()
nrow(human.freedom.index)   # number of rows AFTER dropping

# vector of all column names that are *NOT* features/predictors
non_features = c("year", "ISO_code", "countries", "region", 
                 "hf_score", "hf_rank", "hf_quartile")
# vector of all column names that are responses (or forms of the responses)
responses = c("hf_score", "hf_rank", "hf_quartile")
# vector of all non-features MINUS hf_score (primary response is retained)  
non_features.reduced = non_features[-5]

# dataframe of freatures we care about
hfi.features = human.freedom.index %>% 
  dplyr::select(-non_features)
# dataframe of responses
hfi.response = human.freedom.index %>% 
  dplyr::select(responses)
# dataframe of features AND hf_score
hfi.combined = bind_cols(hfi.response['hf_score'], hfi.features)

# get the number of rows/cols in each 
nrow(hfi.response)
nrow(hfi.features)
ncol(hfi.response)
ncol(hfi.features)




####################################################################################################
####################################################################################################
####################################################################################################

#  Permutation Testing on correlation between ALL features 

####################################################################################################
####################################################################################################
####################################################################################################


nperms = 2000
sig.level = 0.005
actual.cor.matrix = cor(x = hfi.combined)
perm.cor.matrix.upper = matrix(NA , ncol = ncol(hfi.combined), nrow = ncol(hfi.combined))
perm.cor.matrix.lower = matrix(NA , ncol = ncol(hfi.combined), nrow = ncol(hfi.combined))

for ( i in 1:ncol(hfi.combined)){
  for( j in 1:ncol(hfi.combined)){
    if( i > j){
      # ONLY do half the matrix
      perm.vector = rep(-10, nperms)
      for (k in 1:nperms) {
        shuffle.i = sample(x = hfi.combined[[i]], size = nrow(hfi.combined), replace = FALSE) 
        perm.vector[k] = cor(shuffle.i, hfi.combined[[j]])
      }
      perm.cor.matrix.lower[i,j] = quantile(perm.vector, sig.level)
      perm.cor.matrix.upper[i,j] = quantile(perm.vector, 1-sig.level)
    } else if (i == j){
      perm.cor.matrix.lower[i,j] = 1
      perm.cor.matrix.upper[i,j] = 1
    }
  }  
}

get_upper_tri <- function(cormat){
  cormat[lower.tri(cormat)]<- NA
  return(cormat)
}

get_lower_tri<-function(cormat){
  cormat[upper.tri(cormat)] <- NA
  return(cormat)
}

upper.cor = get_upper_tri(actual.cor.matrix)


is.sign =  matrix(NA , ncol = ncol(hfi.combined), nrow = ncol(hfi.combined), 
                  dimnames = list(c(colnames(hfi.combined)), c(colnames(hfi.combined))))

total = 0
count = 0
col.names = colnames(hfi.combined)
for ( i in 1:ncol(hfi.combined)){
  for( j in 1:ncol(hfi.combined)){
    if( i > j){
      total = total + 1
      if(actual.cor.matrix[i,j] < perm.cor.matrix.upper[i,j] & 
         actual.cor.matrix[i,j] > perm.cor.matrix.lower[i,j] ){
        cat(paste("\n[", col.names[i], "," , col.names[j], "] \nactual cor: ", 
                  actual.cor.matrix[i,j], ";\npermutated [lower,upper]: [", 
                  perm.cor.matrix.lower[i,j], ",", 
                  perm.cor.matrix.upper[i,j], "]\n"))  
        count = count + 1
      } else{
        is.sign[i,j] = 1
      }
    } 
  }
}
is.sign
count
total
count/total


lower.perm = get_lower_tri(is.sign)
lower.perm

melted.actual.cor = melt(actual.cor.matrix, na.rm = TRUE) 
melted.upper.cor = melt(upper.cor, na.rm = TRUE) 
melted.lower.perm = melt(lower.perm, na.rm = TRUE)
colnames(melted.lower.perm) = c("Var1", "Var2", "IsSignificant")

nrow(melted.lower.perm)

graph.df = melted.upper.cor %>% full_join(melted.lower.perm)
nrow(graph.df)

colnames(graph.df)
graph.df$IsSignificant = as.factor(as.character(graph.df$IsSignificant))
graph.df2 = graph.df %>% mutate(value = ifelse(is.na(value), 0, value))

# Create the Plot. Ignore the col and row names (to confusing)
#   This is a matrix with 1/2 graph showing significance b/w 2 vars 
ggplot(data = graph.df2, aes(Var2, Var1, fill = value)) +
  geom_tile(color = "white") + 
  geom_point(aes(shape = IsSignificant, fill=value), size=2 ) +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0, limit = c(-1,1), space = "Lab", 
                       name="Pearson\nCorrelation") +
  theme_minimal() + 
  scale_shape(guide = 'none') +
  theme(
    axis.title.x = element_blank(),
    axis.title.y = element_blank(),
    panel.grid.major = element_blank(),
    panel.border = element_blank(),
    panel.background = element_blank(), 
    axis.text.x = element_blank(),
    axis.text.y.left = element_blank()) +
  coord_fixed() +
  ggtitle("Correleation Plot with Permutation Testing Results", 
          subtitle = paste0("Percentage of variable-pairs having significant correlation: ",
                            ((1-round((count/total),3)) * 100), 
                            "%\nSignificance level of ", sig.level*2, " (two-tailed)")) 

