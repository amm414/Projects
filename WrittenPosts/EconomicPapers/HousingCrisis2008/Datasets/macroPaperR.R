library(ggplot2)
library(tidyverse)
library(astsa)






######################    DEPENDS ON WHERE FILE AND DATASET LOCATED    ###########################
# Please Overwrite this file depending on your file system setup 
fileDir = "C:/GitHub/Private-Projects/Website/Written-Content/Academic Posts/Economics/2008 Bubble and Crash/Datasets/"
######################    DEPENDS ON WHERE FILE AND DATASET LOCATED    ###########################






################################
## S$P/Case-Schiller Index
housingData = as_tibble(read_csv( paste(fileDir, "CSUSHPISA.csv", sep = "")))
housingDataPeriod = housingData %>% filter(DATE <= "2010-01-01")
housingDataPeriod$diffed = c(0, diff(housingDataPeriod$CSUSHPISA))
## This lagged adds the previous value of index to the row (to use to calculate growth rate)
housingDataPeriod$lagged = c(lag(housingDataPeriod$CSUSHPISA))
housingDataPeriod = housingDataPeriod %>% filter(DATE>="1990-01-01") 
## Calculate growth rate ==> (current-lagged)/lagged
housingDataPeriod = housingDataPeriod %>% mutate(growthrate = (CSUSHPISA-lagged)/lagged*100 )
housingDataPeriod %>% head()


################################
## Default and related data
### Deleinquency Rates
delinquencyrates = read_csv(paste(fileDir, "DRCCLACBS.csv", sep = ""))

### Default Rates
defaultRate = read_csv( paste(fileDir, "DRSFRMACBS.csv", sep = ""))

# pool all default, delinquncies together
defaults = delinquencyrates %>% inner_join(defaultRate) %>% filter(DATE>="2000-01-01" & DATE <="2010-01-01" )


################################
### Credit Expansion data

## Mortgage Rates (30 and 15 year)
mortgageRate30 = read_csv(paste(fileDir, "MORTGAGE30US.csv", sep = ""))
mortgageRate15 = read_csv(paste(fileDir, "MORTGAGE15US.csv", sep = ""))
mortgageRateBoth = mortgageRate30 %>% inner_join(mortgageRate15)
mortgageRateBoth %>% group_by(DATE) %>% summarise(
  n = n()
)

### Federal Funds Rate
fedfundrate = read_csv(  paste(fileDir, "FEDFUNDS.csv", sep = ""))
fedfundrateLimited = fedfundrate %>% filter(DATE < "2010-01-01" )


##### GRAPHING ######


##########################
## S&P/CAse-Schiller Graphing

## S&P/Case-Shiller Graph from 1990 through 2010
ggplot(data = housingDataPeriod, aes(x=DATE , y= CSUSHPISA)) + 
  geom_line(size = 1.2) + labs(y = "Case-Schiller Home Price Index", x = "Year", caption="Source: FRED, https://fred.stlouisfed.org") +
  ggtitle("FIG. II: Case-Schiller Home Price Index") + 
  annotate("rect", xmin =as.Date("2001-01-01"), xmax = as.Date("2006-01-01") , ymin = 60, ymax =210 , alpha = .2) + ylim(60,210) + 
  theme(plot.background = element_rect(fill="white"), 
        panel.background = element_rect(fill = "white" ),
        panel.grid.major = element_line(colour = "grey", size=.5 )
  )
  

## S&P/Case-Schiller Index Diff AND Growth Rates
ggplot(data = housingDataPeriod, aes(x=DATE, y = growthrate) ) + 
  geom_line() + 
  labs(x = "Year", y = "Monthly Growth Rate (%)", caption="Source: FRED, https://fred.stlouisfed.org") + 
  ggtitle(label = "Growth Rate in Case-Schiller Index") +
  annotate("rect", xmin =as.Date("2001-01-01"), xmax = as.Date("2006-01-01") , ymin = -2, ymax = 2, alpha = .2) + ylim(-2,2) + 
  theme( plot.background = element_rect(fill="white"), 
         panel.background = element_rect(fill = "white" ),
         panel.grid.major = element_line(colour = "grey", size=.5 )
  ) + geom_abline(intercept = 0, slope = 0, size = 1)

#####################################
## graph default and delinquency rate
# ggplot(data = defaults, aes(x = DATE)) + geom_line(aes(y = DRCCLACBS), color = "black", linetype=1) +
#   geom_line(aes(y = DRSFRMACBS), color = "red", linetype=2) + ggtitle("Delinquency and Default Rates") +
#   labs(x = "Year", y = "Rate (%)", caption="Source: FRED, https://fred.stlouisfed.org")

## graph of Federal Funds Rate
ggplot(data = fedfundrateLimited, aes(x=DATE, y=FEDFUNDS)) + geom_line() + 
  geom_abline(slope = 0, intercept = 2, colour="red") + ggtitle("FIG. I: Federal Funds Rate Over Times") +
  labs(x="Date", y="Federal Funds Rate (%)", caption="Source: FRED, https://fred.stlouisfed.org") + 
  annotate("rect", xmin =as.Date("2001-01-01"), xmax = as.Date("2006-01-01") , ymin = 0, ymax = 20, alpha = .2) + ylim(0,20) +
  theme( plot.background = element_rect(fill="white"), 
         panel.background = element_rect(fill = "white" ),
         panel.grid.major = element_line(colour = "grey", size=.5 )
  )

# change col names to make it easier 
colnames(mortgageRateBoth)[2] = "M30"
colnames(mortgageRateBoth)[3] = "M15"
mortgage_df = mortgageRateBoth %>% filter(DATE<"2010-01-01") %>% gather(key, value, M15, M30)
# ggplot(data = mortgage_df , aes(x=DATE, y=value, color=key, linetype=key)) + 
#   geom_line() + ggtitle("Average Mortgage Rate for Fixed Rate Mortgages") +
#   labs(x = "Year", y = "Average Mortgage Rate", caption="Source: FRED, https://fred.stlouisfed.org")

# joining Mortgages and Fed Funds RATES
rates_df = fedfundrate %>% inner_join(mortgageRateBoth, by=c("DATE"))
colnames(rates_df)[2] = "FED"
rates_df = rates_df %>% gather(key, value, M15, M30, FED) %>% filter(DATE<"2010-01-01")
rates_df %>% head()
fedfundrate %>% head()

##########################
# Mortgage Rate (15/30 year averages) and Federal Funds 

ggplot(data = rates_df , aes(x=DATE, y=value, color=key, linetype=key)) + geom_line() +
  ggtitle("30 and 15 Year Mortgage Rates and Federal Funds Rate (1990 thorugh 2010)") + 
  labs(x = "Year", y = "Rate (%)", caption="Source: FRED, https://fred.stlouisfed.org") +
  annotate("rect", xmin =as.Date("2001-01-01"), xmax = as.Date("2006-01-01") , ymin = 0, ymax = 10, alpha = .2) + ylim(0,10) +
  theme( plot.background = element_rect(fill="white"), 
         panel.background = element_rect(fill = "white" ),
         panel.grid.major = element_line(colour = "grey", size=.5 )
  ) + scale_color_manual(values = c("black", "red", "blue"))
#######################



#### Robert Schillers Datasets ##########
robshildata1 = as_tibble(read_csv( paste(fileDir, "robschildata.csv", sep = "")))
robshildata2 = as_tibble(read_csv( paste(fileDir, "robschildata2.csv", sep = "")))

total = robshildata1 %>% full_join(robshildata2, by=c("Date") )

ggplot(data = total , aes(x = Date)) + geom_line(aes(y = Index), linetype=1) + 
  geom_line(aes(y = RBCI), linetype=2) + geom_line(aes(y=LIR), linetype=3)
