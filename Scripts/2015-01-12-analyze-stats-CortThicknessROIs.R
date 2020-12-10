basepath <- "~/Ares/RPV9/Results/7-Stats-c"

# Load Volume data
df <- read.csv(file.path(basepath, "Stats-RPV9-CorticalThicknessROIs.csv"))
# # Reorder labels
# df$Group <- factor(df$Group,
#                      levels=list("Control", "AIE"))

require(reshape2)
require(gridExtra)

# Rename Structure to Bregma
names(df)[names(df)=='Structure'] <- 'Bregma'

levels(df$Bregma)[levels(df$Bregma)=="L-01"] <- -0.30
levels(df$Bregma)[levels(df$Bregma)=="L-02"] <- -0.40
levels(df$Bregma)[levels(df$Bregma)=="L-03"] <- -0.80
levels(df$Bregma)[levels(df$Bregma)=="L-04"] <- -0.92
levels(df$Bregma)[levels(df$Bregma)=="L-05"] <- -1.40
levels(df$Bregma)[levels(df$Bregma)=="L-06"] <- -1.80
levels(df$Bregma)[levels(df$Bregma)=="L-07"] <- -2.12
levels(df$Bregma)[levels(df$Bregma)=="R-08"] <- -0.30
levels(df$Bregma)[levels(df$Bregma)=="R-09"] <- -0.40
levels(df$Bregma)[levels(df$Bregma)=="R-10"] <- -0.80
levels(df$Bregma)[levels(df$Bregma)=="R-11"] <- -0.92
levels(df$Bregma)[levels(df$Bregma)=="R-12"] <- -1.40
levels(df$Bregma)[levels(df$Bregma)=="R-13"] <- -1.80
levels(df$Bregma)[levels(df$Bregma)=="R-14"] <- -2.12

df$Hemisphere <- NA
df[df$Label <= 7, ]$Hemisphere <- 'Left'
df[df$Label >= 8, ]$Hemisphere <- 'Right'

df$Dataset <- 'Volume'

# Reorder columns
df.vol <- df[c('Dataset','Group','Subject','Hemisphere','Bregma','Volume')]

df.thickness <- read.csv('~/Ares/RPV9/Processing/CorticalThickness/Figure-CortexOverlay/Data/CorticalThickness+TissueThickness.csv')

df.thickness <- df.thickness[c(-1)]
df.thickness <- subset(df.thickness, Dataset=='Imaging')



names(df.vol)[names(df.vol)=='Volume'] <- 'Value'
names(df.thickness)[names(df.thickness)=='Thickness'] <- 'Value'


df <- rbind(df.vol,df.thickness)

#---------------------------------------------------------------------------#
# Analysis
#---------------------------------------------------------------------------#
require(ggplot2)
plotsize=1000
golden=1.618
res=300

# Overall
ggplot(aes(x=Bregma, y=Value, color=Group), data=df.vol) + geom_boxplot() + facet_grid(Hemisphere~.) + ggtitle('Cortical Volume in 7 Bregma ROIs')
dev.copy(png, "~/Ares/RPV9/Processing/CorticalThickness/Figure-CortexOverlay/Fig-box-volume.png", height=plotsize/golden, width=plotsize)
dev.off()




# Wide format with Imaging & Tissue data
df.c <- dcast(df, Hemisphere+Bregma+Group+Subject~Dataset,value.var = 'Value',  fun.aggregate = mean, na.rm = TRUE)


title <- 'Overall Correlation between Volume & Imaging'
correlation <- cor(df.c$Imaging,df.c$Volume, use="complete.obs", method="pearson")
ggplot(aes(x = Imaging, y = Volume), data=df.c) + geom_point(size=3) +     geom_smooth(method=lm)  + annotate("text", x=1300, y=0.5, label=paste("Pearson's r =",round(correlation,2))) + ggtitle(title)
dev.copy(png, "~/Ares/RPV9/Processing/CorticalThickness/Figure-CortexOverlay/Fig-scatter-volume.png", height=plotsize/golden, width=plotsize)
dev.off()

title <- 'Correlation between Volume & Imaging by Group'
ggplot(aes(x = Imaging, y = Volume, color=Group), data=df.c) + geom_point(size=3) +     geom_smooth(method=lm)  + ggtitle(title)
dev.copy(png, "~/Ares/RPV9/Processing/CorticalThickness/Figure-CortexOverlay/Fig-scatter-volumeXgroup.png", height=plotsize/golden, width=plotsize)
dev.off()

title <- 'Volume & Imaging by Group & Hemisphere'
ggplot(aes(x = Imaging, y = Volume, color=Group), data=df.c) + geom_point(size=3) +     geom_smooth(method=lm)  + facet_grid(Hemisphere~Group)
dev.copy(png, "~/Ares/RPV9/Processing/CorticalThickness/Figure-CortexOverlay/Fig-scatter-volumeXgroupXhemisphere.png", height=plotsize/golden, width=plotsize)
dev.off()
