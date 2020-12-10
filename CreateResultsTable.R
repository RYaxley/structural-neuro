setwd('~/Dropbox/Work/03.UNC/2013-10-10-NADIA-Retreat')

# Load data as data frames
LvF  <- read.csv('/Volumes/Ares/LvF/7-Stats/Stats-LvF-Overnight.csv', header=TRUE)
CLE1 <- read.csv('/Volumes/Ares/CLE1/7-Stats/Stats-NADIA_pilot.csv', header=TRUE)
CLE2 <- read.csv('/Volumes/Ares/CLE2/7-Stats/Stats-CLE_04_2011.csv', header=TRUE)
RPV1 <- read.csv('/Volumes/Ares/RPV1/Processing/7-Stats/Stats-RPV1.csv', header=TRUE)
RPV3 <- read.csv('/Volumes/Ares/RPV3/Processing/7-Stats/Stats-RPV3.csv', header=TRUE)
LJC1 <- read.csv('/Volumes/Ares/LJC1/Processing/7-Stats-ANTS_2013Aug29-current/Stats-LJC1.csv', header=TRUE)
WL4  <- read.csv('/Volumes/Ares/WL4/Processing/7-Stats/Stats-WL4.csv', header=TRUE)

# Merge the data
d <- rbind(LvF, CLE1, CLE2, RPV1, RPV3, LJC1, WL4)

# Rename Experiment names to match
require(car)
d$Study <- recode(d$Study, " 'NADIA_pilot'='CLE1' ")
d$Study <- recode(d$Study, " 'CLE_04_2011'='CLE2' ")

# Drop LvF which doesn't have AIE
d <- subset(d, Study!='LvF') 

results.d

for(i in unique(d$Study) ){
  for(j in c('Amygdala', 'Neocortex', 'Cerebellum') ){
    idata <- subset(d, Study==i)
    jdata <- subset(idata, Structure==j)    
    con <- subset(jdata, Group=='Control')$Ratio
    aie <- subset(jdata, Group=='AIE')$Ratio
    
    print( c(i, j, mean(con), mean(aie), t.test(con,aie)$p.value ), ro )
  }
}
