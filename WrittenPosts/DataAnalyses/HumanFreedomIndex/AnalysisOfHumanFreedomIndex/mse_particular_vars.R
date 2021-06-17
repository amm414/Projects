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


generate.train.test = function(data){
  combined.train = data %>% sample_frac(size=0.8)
  combined.test = data %>% setdiff(combined.train)
  
  tss.hf_score = mean((mean(data$hf_score) -
                         data$hf_score)^2)
  tss.test.hf_score = mean((mean(combined.test$hf_score) -
                              combined.test$hf_score)^2)
  # Total Sum of Squares AVERAGED (since we are dealing with MSE)
  tss.hf_score
  tss.test.hf_score
  ret.list = list("train" = combined.train, "test" = combined.test, 
                  "tss" = tss.hf_score, "tss.test" = tss.test.hf_score)
}

generate_mse_r2_for_vars = function(vars){
  set.seed(111)
  # dataframe of freatures we care about
  hfi.features = human.freedom.index %>% 
    dplyr::select(vars)
  # dataframe of responses
  hfi.response = human.freedom.index %>% 
    dplyr::select(responses)
  # dataframe of features AND hf_score
  hfi.combined = bind_cols(hfi.response['hf_score'], hfi.features)
  
  hfi.combined.split = generate.train.test(hfi.combined) 
  
  lm.fit = lm(hf_score ~ . , data=hfi.combined.split[["train"]])
  lm.preds = predict(lm.fit, newdata = hfi.combined.split[['test']])
  
  mse.lm = mean((lm.preds - hfi.combined.split[["test"]]$hf_score)^2)
  lm.r2 = 1 - (mse.lm/hfi.combined.split[["tss.test"]])
  c(mse.lm, lm.r2)
}

generate_mse_r2_for_vars(c("pf_expression_control", "pf_expression_influence"))

generate_mse_r2_for_vars(c("pf_expression_control", 
                           "ef_legal_military", "ef_trade_regulatory"))

generate_mse_r2_for_vars(c("pf_expression_influence", 
                           "ef_legal_military", "ef_trade_regulatory"))

generate_mse_r2_for_vars(c("pf_expression_control",  
                           "ef_legal_military", 
                           "ef_trade_regulatory_compliance"))

generate_mse_r2_for_vars(c("pf_expression_control",  
                           "ef_trade_regulatory"))

generate_mse_r2_for_vars(c("pf_expression_influence", "ef_legal_military", 
                           "ef_trade_regulatory_compliance"))

generate_mse_r2_for_vars(c("pf_expression_influence", "ef_trade_regulatory"))

generate_mse_r2_for_vars(c("pf_expression_influence", "ef_trade_regulatory_compliance"))

generate_mse_r2_for_vars(c("pf_expression_control", "pf_expression_influence", 
                           "ef_trade_regulatory",
                           "ef_trade_regulatory_compliance"))

generate_mse_r2_for_vars(c("pf_expression_control", "pf_expression_influence", 
                           "ef_legal_military", "ef_trade_regulatory",
                           "ef_trade_regulatory_compliance"))


