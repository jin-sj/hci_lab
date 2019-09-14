library(dplyr)
library(coin)

df_wo_ai <- read.csv('/Users/sjjin/workspace/hci_lab/nasa_tlx/nasa_tlx_wo_ai.csv', sep=',', row.names=1)
df_w_ai <- read.csv('/Users/sjjin/workspace/hci_lab/nasa_tlx/nasa_tlx_w_ai.csv', sep=',', row.names=1)

rating_w_ai <- read.csv('/Users/sjjin/workspace/hci_lab/nasa_tlx/rating_w_ai.csv', sep=',')
rating_wo_ai <- read.csv('/Users/sjjin/workspace/hci_lab/nasa_tlx/rating_wo_ai.csv', sep=',')




get_shapiro_test <- function(df1, ai, columns) {
  #ccc <- colnames(df1)
  if (ai) {
    print("WITH AI")
  } else {
    print("WITHOUT AI")
  }
  for (col in columns) {
  #for (col in ccc[3:length(ccc)]) {
    #print(df1[col])
    result <- shapiro.test(as.vector(df1[[col]]))
    p <- result$p.value
    if (p < 0.05) {
      print(sprintf("%s is NOT from a Normal distribution; p: %0.6f", col, p))
    } else {
      print(sprintf("%s is a Normal distribution; p: %0.6f", col, p))
    }
    cat("\n")
    #print(result)
  }
}

get_wilcoxon_test <- function(df1, df2, columns) {
  #ccc <- colnames(df1)
  for (col in columns) {
  #for (col in ccc[3:length(ccc)]) {
    #GroupA <- as.vector(df_w_ai[col])
    #GroupB <- as.vector(df_wo_ai[col])
    GroupA <- df1[[col]]
    GroupB <- df2[[col]]
    result <- wilcoxsign_test(GroupA ~ GroupB, distribution="exact")
    p <- pvalue(result)
    z <- statistic(result)
    effect_size = abs(z) / sqrt(length(GroupA))
    #print(result)
    if (p < 0.05) {
      print(sprintf("DIFFERENT distribution for %s", col))
    } else {
      print(sprintf("Same distribution for %s", col))
    }
    print(sprintf("z: %0.6f, p: %0.6f effect_size: %0.6f", z, p, effect_size))
    cat("\n")
  }
}


nasa_columns <- colnames(df_wo_ai)[3:length(df_wo_ai)]
rating_columns <- colnames(rating_w_ai)[1:2]


#get_shapiro_test(df_w_ai, TRUE, nasa_columns)
#get_shapiro_test(df_wo_ai, FALSE, nasa_columns)
#get_wilcoxon_test(df_w_ai, df_wo_ai, nasa_columns)

get_wilcoxon_test(rating_w_ai, rating_wo_ai, rating_columns)

mean_rating_w_ai <- rating_w_ai %>% group_by(Participant) %>% summarise(mean(Rating), mean(Video.Understanding))
mean_rating_wo_ai <- rating_wo_ai %>% group_by(Participant) %>% summarise(mean(Rating), mean(Video.Understanding))
mean_columns <- colnames(mean_rating_w_ai)[2:length(mean_rating_w_ai)]
get_wilcoxon_test(mean_rating_w_ai, mean_rating_wo_ai, mean_columns)

