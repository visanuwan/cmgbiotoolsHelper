if (!require("gplots")) {
  install.packages("gplots", repos="http://cran.rstudio.com/")
}

library(gplots)

codon <- read.table("codonUsage.all")
colnames(codon) <- c( 'Name', 'codon', 'score', 'count')
codon <- codon [1:3]
test <- reshape(codon , idvar="Name", timevar="codon", direction="wide")
codonMatrix <- data.matrix(test[2:length(test)])
rownames(codonMatrix) <- test$Name

codon_heatmap <- heatmap.2(codonMatrix , scale="none", main="Codon usage", xlab="Codon fraction", ylab="Organism", trace="none", margins=c(8, 25))
dev.print(postscript, "codonUsage.ps", width = 25, height=25)
dev.off()
