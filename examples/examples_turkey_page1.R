library(reticulate)
library(readr)

imfcharts = import("imfcharts")
matplotlib = import("matplotlib")
matplotlib$use('Qt5Agg')

# Read in data
infilename <- 'data/turkey_page1/fig1_chart2_labor.csv'
df <- read.csv(infilename)

chart <- imfcharts$Chart(df, indexcol='dates', linecols=colnames(df), debug=TRUE)
chart$show()
