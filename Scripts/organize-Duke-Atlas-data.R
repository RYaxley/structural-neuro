basepath <- "~/Ares/RPV9/Results/7-Stats-c"

require(reshape2)
require(ggplot2)


# Open data from Calabrese et al. 2013 paper
data <- read.csv("../Atlas-Duke-P80-Johnson/Data-Volumes-Calabrese-etal-2013.csv", header=T)

# Sum all regions to get Total Brain Volume (excluding Age in column 1)
data$Total.Brain <- rowSums(data[,2:27])

# Restructure
data.melt <- melt(data, id="Age..days.")


# Total Brain Volume
pdf(file.path(basepath, "Calabrese-TBV-Volume.Age.pdf"))
qplot(Age..days., value, data=subset(data.melt, variable=="Total.Brain"),
      geom=c("point", "smooth"), se=T,
      main="TBV calculated from data in Calabrese et al. 2013", ylab="Volume")
dev.off()


# Reduce to TBV only
data.tbv <- subset(data.melt, variable=="Total.Brain")

# TBV for P80s only
tbv.80 <- subset(data.tbv, Age..days.==80)
summary(tbv.80$value)


aggregate(data.melt$value, list(data.melt$Age..days., data.melt$variable), mean)