require(ggplot2)
require(ggpubr)

Mtb_TajD <- read.csv("2023_12_22_popoolationStats.csv",header = TRUE, sep = (","))

Mtb_TajD$Strain <- as.factor(Mtb_TajD$Strain)
Mtb_TajD$Condition <- as.factor(Mtb_TajD$Condition)

TajD_RNA_BP <- ggplot(Mtb_TajD, aes(x=Strain,y=tajimasD,color=Condition)) + geom_boxplot() + geom_point(position = position_dodge(width = .75)) + ylim(c(-2,-0.5)) + theme_minimal()

d.boxplot <- ggarrange(TajD_RNA_BP, labels = "RNA", ncol = 1, nrow = 1)

ggsave("Mtb_tajimasD_AllConditions_RNA_boxplot.pdf",d.boxplot, width=10, height=10)