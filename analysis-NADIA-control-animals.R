setwd("~/Ares/NADIA/Results/2014-03-14-Volumes-of-Controls/")

# This is the datafile I created for Dehan Kong. However, I since update RPV1 and RPV3.
# d <- read.csv("NADIA-Segmentation-Statistics.csv", header=T)

# Load data
LvF  <- read.csv('/Volumes/Ares/NADIA/LiveVSFixedStudy/Results/7-Stats/Stats-LvF-Overnight.csv', header=TRUE)
CLE1 <- read.csv('/Volumes/Ares/NADIA/NADIA_pilot/7-Stats/Stats-NADIA_pilot.csv', header=TRUE)
CLE2 <- read.csv('/Volumes/Ares/NADIA/CLE_04_2011/7-Stats/Stats-CLE_04_2011.csv', header=TRUE)
RPV1 <- read.csv('/Volumes/Ares/NADIA/RPV1/Results/7-Stats/Stats-RPV1.csv', header=TRUE)
RPV3 <- read.csv('/Volumes/Ares/NADIA/RPV3/Results/7-Stats/Stats-RPV3.csv', header=TRUE)
LJC1 <- read.csv('/Volumes/Ares/NADIA/LJC1/Results/7-Stats-ANTS_2013Aug29-current/Stats-LJC1.csv', header=TRUE)
WL4  <- read.csv('/Volumes/Ares/NADIA/WL4/Results/7-Stats/Stats-WL4.csv', header=TRUE)

# Merge the data
d <- rbind(LvF, CLE1, CLE2, RPV1, RPV3, LJC1, WL4)

# Rename Experiment names to match
require(car)
d$Study <- recode(d$Study, " 'NADIA_pilot'='CLE1' ")
d$Study <- recode(d$Study, " 'CLE_04_2011'='CLE2' ")

# TBV of controls only
controls <- subset(d, Group=='Control')
tbv <- subset(controls, Structure=='Total Brain')

# Plots
require(reshape2)
require(ggplot2)

plot(Volume~Age, data=tbv)
boxplot(Volume~Age, data=tbv)

# Consider dropping P72 time point
# tbv <- subset(tbv,Study!="CLE1")

plotsize = 1400
golden = 1.618
png("TBV-Volume.Bodyweight-linear.png",
    height=plotsize/golden, width=plotsize, res=150)
qplot(Age,Volume, data=tbv, geom=c("point","smooth"), se=T,
      method="lm",formula = y ~ poly(x,2),
      main="Total Brain Volume of Control Subjects") + theme_light()
dev.off()



