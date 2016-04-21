if (!require("gplots")) {
  install.packages("gplots", repos="http://cran.rstudio.com/")
}

library(gplots)

aa <- read.table("aaUsage.all")
colnames(aa) <- c( 'Name', 'aa', 'score')
test <- reshape(aa, idvar="Name", timevar="aa", direction="wide")
aaMatrix <- data.matrix(test[2:length(test)])
rownames(aaMatrix) <- test$Name

stat_heatmap <- heatmap.2(aaMatrix, scale="none", main="Amino acid usage", xlab="Amino acid fraction", ylab="Organism", trace="none", margins=c(8, 25), col = cm.colors(256))
dev.print(postscript, "aaUsage.ps", width = 25, height=25)
dev.off()
