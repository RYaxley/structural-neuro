# RPV9 - Cortical Thickness Imaging + Tissue measurements

require(reshape2)
require(ggplot2)

setwd("~/Desktop")

d <- read.csv("RPV9-cortical-thickness.csv", header=T)

# Segregate data frame by hemisphere
r <- subset(d, Hemisphere=='Right')
l <- subset(d, Hemisphere=='Left')

# Overall comparison of Tissue and Imaging Thickness

# Average across Bregma slices
lcast <- dcast(l, Region+Group+Subject~Dataset,value.var = 'Thickness',  fun.aggregate = mean, na.rm = TRUE)
# drops <- "middle"
# lcast <- lcast[,!(names(lcast) %in% drops)]
lcast <- subset(lcast, Region!="middle")
# Now melt the cast data
lmelt <- melt(lcast, id.vars= c("Group","Subject","Region"), value.name="Thickness", variable.name="Dataset")


plotsize=800
golden=1.618


# Overall boxplot across Datasets
ggplot(aes(x = Dataset, y= Thickness), data=lmelt) + geom_boxplot() + geom_point(position=position_jitter(w=0.01,h=0)) + ggtitle("Thickness across Imaging & Tissue data")
dev.copy(png, "RPV9-thicknessXdataset.png", height=plotsize/golden, width=plotsize)
dev.off()

t.test(lcast$Tissue, lcast$Imaging)

# Overall scatterplot w/ regression line
correlation <- cor(lcast$Imaging,lcast$Tissue, use="complete.obs", method="pearson")
ggplot(aes(x = Imaging, y = Tissue), data=lcast) + geom_point(size=3) +
     geom_smooth(method=lm) +
     annotate("text", x=1.4, y=2.7, label=paste("Pearson's r =",round(correlation,2)))
dev.copy(png, "RPV9-thicknessXdataset-scatter.png", height=plotsize/golden, width=plotsize)
dev.off()

# Overall lines matched by subject
ggplot(aes(x = Imaging, y = Tissue, color=factor(Subject) ), data=lcast) + geom_point(size=3) +
     geom_smooth(method=lm) +
     annotate("text", x=1.4, y=2.7, label=paste("Pearson's r =",round(correlation,2)))
dev.copy(png, "RPV9-thicknessXdataset-scatterline.png", height=plotsize/golden, width=plotsize)
dev.off()

cor.test(lcast$Imaging,lcast$Tissue, use="complete.obs", method="pearson")


# Scatterplot segregated by Region
ggplot(aes(x = Imaging, y = Tissue, color=Region), data=lcast) + geom_point(size=3) +
     geom_smooth(method=lm)
dev.copy(png, "RPV9-tissueXimagingXregion-scatter.png", height=plotsize/golden, width=plotsize)
dev.off()

lcast.ant <- subset(lcast, Region=="anterior")
cor(lcast.ant$Imaging,lcast.ant$Tissue,use="complete.obs", method="pearson")

lcast.post <- subset(lcast, Region=="posterior")
cor(lcast.post$Imaging,lcast.post$Tissue,use="complete.obs", method="pearson")


# Scatterplot segregated by Group
ggplot(aes(x = Imaging, y = Tissue, color=Group), data=lcast) + geom_point(size=3) +
     geom_smooth(method=lm)
dev.copy(png, "RPV9-tissueXimagingXgroup-scatter.png", height=plotsize/golden, width=plotsize)
dev.off()


# Boxplot
ggplot(aes(x = Group, y= Thickness, color=Group), data=lmelt) + geom_boxplot() + geom_point() + ggtitle("Thickness across Imaging & Tissue data")+facet_wrap(~Dataset)
dev.copy(png, "RPV9-thicknessXgroupXdataset-boxplot.png", height=plotsize/golden, width=plotsize)
dev.off()

ggplot(aes(x = Dataset, y= Thickness, color=Dataset), data=lmelt) + geom_boxplot() + geom_point() + ggtitle("Thickness across Imaging & Tissue data")+facet_wrap(~Group)
dev.copy(png, "RPV9-thicknessXdatasetXgroup-boxplot.png", height=plotsize/golden, width=plotsize)
dev.off()

ggplot(aes(x = Group, y= Thickness, color=Group), data=lmelt) + geom_boxplot() + geom_point() + ggtitle("Thickness across Imaging & Tissue data")+facet_wrap(~Dataset+Region)
dev.copy(png, "RPV9-thicknessXgroupXdatasetXregion-boxplot.png", height=plotsize/golden, width=plotsize)
dev.off()

# t-tests

# Subset Anterior & Posterior
lcast.ant.aie <- subset(lcast.ant, Group=="AIE")
lcast.ant.con <- subset(lcast.ant, Group=="Control")
lcast.post.aie <- subset(lcast.post, Group=="AIE")
lcast.post.con <- subset(lcast.post, Group=="Control")

t.test(lcast.ant.con$Imaging,lcast.ant.aie$Imaging)
t.test(lcast.ant.con$Tissue, lcast.ant.aie$Tissue)
t.test(lcast.post.con$Imaging,lcast.post.aie$Imaging)
t.test(lcast.post.con$Tissue, lcast.post.aie$Tissue)


