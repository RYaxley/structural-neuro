basepath <- "~/Ares/RPV9/Results/7-Stats-c"

# Load Volume data
data <- read.csv(file.path(basepath, "Stats-RPV9.csv"))
# Reorder labels
data$Group <- factor(data$Group,
                     levels=list("Unmanipulated", "Control", "AIE"))

# Load Duke P80 atlas data as baseline
atlas <- read.csv("~/Ares/RPV9/Tools/Atlas-Duke-P80-Johnson/Stats-Duke-Atlas.csv")
# Rename group factor so these data are not lumped together with the study Controls.
atlas$Group <- factor("Atlas", levels="Atlas")

# Merge datasets
data.atlas <- rbind(data,atlas)
# Reorder labels
data.atlas$Group <- factor(data.atlas$Group,
                           levels=list("Atlas","Unmanipulated", "Control", "AIE"))

# Create a new grouping variable with Unmanipulated and Control groups collapsed
data$Group2[data$Group == "Unmanipulated"] <- "Control"
data$Group2[data$Group == "Control"] <- "Control"
data$Group2[data$Group == "AIE"] <- "AIE"
# Convert column to factor
data$Group2 <- factor(data$Group2, levels=list("Control","AIE"))



#---------------------------------------------------------------------------#
# Generate table of means for each Structure

require(reshape2)
require(gridExtra)

# Raw Volume
means <- aggregate(round(data$Volume),
                   list(Structure=data$Structure, Group=data$Group), mean)
volumes <- dcast(volumes, volumes$Structure~volumes$Group) # Organize values
volumes <- volumes[order(-volumes$Unmanipulated), ] # Sort values

pdf(file.path(basepath, "Volume.Means.pdf"), height=11, width=8.5)
grid.table(volumes, main="Region Volumes", h.even.alpha=.5, v.even.alpha=1.)
dev.off()


# Ratio of volume to TBV
ratios <- aggregate(round(data$Ratio,2),
                   list(Structure=data$Structure, Group=data$Group), mean)
ratios <- dcast(ratios, ratios$Structure~ratios$Group) # Organize values
ratios <- ratios[order(-ratios$Unmanipulated), ] # Sort values

pdf(file.path(basepath, "Ratio.Means.pdf"), height=11, width=8.5)
grid.table(ratios, main="Region Volumes", h.even.alpha=.5, v.even.alpha=1.)
dev.off()



#---------------------------------------------------------------------------#
# Total brain volume x bodyweight plots
require(ggplot2)

tbv <- subset(data, Structure=='Total Brain')

# Linear fit
pdf(file.path(basepath, "TBV-Volume.Bodyweight-linear.pdf"))
p1 <- qplot(Bodyweight, Volume, data=tbv,
      geom = c("point", "smooth"), method = "lm") + theme_light()
dev.off()
# Smooth fit
pdf(file.path(basepath, "TBV-Volume.Bodyweight-poly.pdf"))
p2 <- qplot(Bodyweight, Volume, data=tbv,
      geom = c("point", "smooth"), se=T) + theme_light()
dev.off()


# Split by group
# Linear model by group
pdf(file.path(basepath, "TBV-Volume.Bodyweight-linear-group.pdf"))
qplot(Bodyweight, Volume,  data=tbv,
      color=Group, geom = c("point", "smooth"), method = "lm") + theme_light()
dev.off()
# Polynomial linear model by group
pdf(file.path(basepath, "TBV-Volume.Bodyweight-poly-group.pdf"))
qplot(Bodyweight, Volume,  data=tbv, color=Group,
      geom = c("point", "smooth"), method = "lm", formula = y ~ poly(x,2)) + theme_light()
dev.off()

# Rug plot
require(sjPlot)
pdf(file.path(basepath, "TBV-Volume.Bodyweight-rugplot.pdf"))
sjp.scatter(tbv$Bodyweight, tbv$Volume, grp = tbv$Group,
            showGroupFitLine = T, showTotalFitLine = F, useFacetGrid = F,
            fitmethod="lm", showRug = T, theme = "light")
dev.off()





#---------------------------------------------------------------------------#
# Statistical tests (ANOVA and Tukey's test of honest signficant difference)
test.roi.volume <- function(roi, data){

     print(roi)

     d <- subset(data, Structure == roi)

     # Define linear models
     fit.1 <- aov(Volume ~ Group, data=d)
     fit.2 <- aov(Volume ~ Group * Bodyweight, data=d)

     anova.1 <- summary(fit.1)
     print(anova.1)

     # Tukey's Honest Significant Differences (For pairwise comparisons)
     posthoc.1 <- TukeyHSD(fit.1, conf.level=0.95)
     print(posthoc.1)

     # t-tests for independent samples
     # Benjamini, Hochberg, and Yekutieli control the false discovery rate
     #      ttest.1 <- pairwise.t.test(d$Volume, d$Group,
     #                      paired = FALSE, p.adjust.method = "fdr")
     #      print(ttest.1)
}

test.roi.ratio <- function(roi, measure, data){

     print(roi)

     d <- subset(data, Structure == roi)

     # Define linear models
     fit.1 <- aov(Ratio ~ Group, data=d)
     fit.2 <- aov(Ratio ~ Group * Bodyweight, data=d)

     anova.1 <- summary(fit.1)
     print(anova.1)

     # Tukey's Honest Significant Differences (For pairwise comparisons)
     posthoc.1 <- TukeyHSD(fit.1, conf.level=0.95)
     print(posthoc.1)

     # t-tests for independent samples
     # Benjamini, Hochberg, and Yekutieli control the false discovery rate
     #      ttest.1 <- pairwise.t.test(d$Volume, d$Group,
     #                      paired = FALSE, p.adjust.method = "fdr")
     #      print(ttest.1)
}



#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
plot.4.group <- function(roi, data) {

     d <- subset(data, Structure == roi)

     boxplot(Volume ~ Group, data = d,
             main=paste(roi, "Volume"),
             ylab=expression(paste("Volume µm"^"3")),
             xlab="Treatment Group",
             boxwex=.3, staplewex=0, # Box and staple width
             col=c("white", "white","lightblue","yellow") )

     # Set L-shaped borders
     par(bty="l")
     # Add  datapoints
     with(d, points(Group,Volume, pch=1))
     # Line for grand mean
     abline(h=mean(d$Volume),col="black", lty=3)

     # Save plot
     #      dev.copy(pdf, file.path(basepath, paste( roi, ".pdf", sep="")))
     dev.copy(png, file.path(basepath, paste( roi, "-4-group.png", sep="")),
              width=640, height=480)
     dev.off()
}


# Visualize with boxplot
plot.3.group <- function(roi, data) {

     d <- subset(data, Structure == roi)

     boxplot(Volume ~ Group, data = d,
             main=paste(roi, "Volume"),
             ylab=expression(paste("Volume µm"^"3")),
             xlab="Treatment Group",
             boxwex=.3, staplewex=0, # Box and staple width
             col=c("white","lightblue","yellow") )

     # Set L-shaped borders
     par(bty="l")
     # Add  datapoints
     with(d, points(Group,Volume, pch=1))
     # Line for grand mean
     abline(h=mean(d$Volume),col="black", lty=3)

     # Save plot
#      dev.copy(pdf, file.path(basepath, paste( roi, ".pdf", sep="")))
     dev.copy(png, file.path(basepath, paste( roi, "-3-group.png", sep="")),
              width=640, height=480)
     dev.off()
}
#---------------------------------------------------------------------------#
# Visualize with boxplot
plot.2.group <- function(roi, data) {

     d <- subset(data, Structure == roi)

     boxplot(Volume ~ Group2, data = d,
             main=paste(roi, "Volume"),
             ylab=expression(paste("Volume µm"^"3")),
             xlab="Treatment Group",
             boxwex=.3, staplewex=0, # Box and staple width
             col=c("lightblue","yellow") )

     # Set L-shaped borders
     par(bty="l")
     # Add  datapoints
     with(d, points(Group2,Volume, pch=1))
     # Line for grand mean
     abline(h=mean(d$Volume),col="black", lty=3)

     # Save plot
     #      dev.copy(pdf, file.path(basepath, paste( roi, ".pdf", sep="")))
     dev.copy(png, file.path(basepath, paste( roi, "-2-group.png", sep="")),
              width=640, height=480)
     dev.off()
}

#---------------------------------------------------------------------------#
# Specify regions-of-interest

# roi <- c('Total Brain', 'Cerebellum', 'Isocortex', 'Amygdala', 'Striatum', 'Accumbens', 'Hippocampus')
roi <- unique(data$Structure)


# Run ANOVA and posthoc tests
sink(file.path(basepath, "Results.Volumes.txt"))
lapply(roi, test.roi.volume, data=data)
sink()
sink(file.path(basepath, "Results.Ratios.txt"))
lapply(roi, test.roi.ratio, data=data)
sink()


# Create Boxplots
lapply(roi, plot.2.group, data=data) # Control v AIE
lapply(roi, plot.3.group, data=data) # Unmanipulated v Control v AIE
lapply(roi, plot.4.group, data=data.atlas) # Atlas v Unmanipulated v Control v AIE


#---------------------------------------------------------------------------#
# TODO
# i would like a trellis? plot where all of the regions are plotted side by side
# TODO I'd like to create one nice table of ANOVA and ANOVA and t-test results. maybe some stars to indicate significance






