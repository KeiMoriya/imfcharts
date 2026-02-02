library(reticulate)
library(readr)
library(dplyr)       
library(tibble)     

# ---------------------------------------------------------------------
# import python modules
# ---------------------------------------------------------------------
imfcharts <- import("imfcharts")

# Attach all chart objects to the global environment
# This is the equivalent of doing
# from imfcharts import *
# in Python
for (name in names(imfcharts)) {
  assign(name, imfcharts[[name]], envir = .GlobalEnv)
}

pd <- import("pandas")
# matplotlib = import("matplotlib")
# matplotlib$use('Qt5Agg')

# ---------------------------------------------------------------------
# read & wrangle in R
# ---------------------------------------------------------------------
df_r <- read_csv("data/turkey_page6/fig6_chart1_current_account.csv") %>% 
  mutate(dates = lubridate::ymd(dates)) %>% 
  arrange(dates) %>% 
column_to_rownames("dates")

# Without conversion to index for dates
df_r2 <- read_csv("data/turkey_page6/fig6_chart1_current_account.csv") %>% 
  mutate(dates = lubridate::ymd(dates)) %>% 
  arrange(dates)

# ---------------------------------------------------------------------
# convert → pandas and make sure index is DatetimeIndex   
# ---------------------------------------------------------------------
py_df <- r_to_py(df_r)
py_df$index <- pd$to_datetime(py_df$index)

# ---------------------------------------------------------------------
# build dict_attrs ‒ This creates python dictionary in R
# ---------------------------------------------------------------------
attrs <- dict(
  `Risk weighted Assets (RHS)` = dict(color = IMFBLACK),
  Capital                       = dict(color = IMFBLUE),
  `Core capital`                = dict(color = IMFRED)
)

# ---------------------------------------------------------------------
# build the chart – NOTE: pass py_df, not df  and use r_to_py() to pass 
# python list to Chart()
# ---------------------------------------------------------------------
chart1 <- Chart(
  df_r,
  linecols  =  c("Capital", "Core capital"),
  rlinecols = "Risk weighted Assets (RHS)",
  attrs = attrs,
  title      = "Bank Capital",
  subtitle   = "(Percent of risk-weighted assets; RWA y/y percent change)",
  legend_left = 0.4,
  xrange     = "2022-01:",
  yrange     = c(10, 25),
  ryrange    = c(120, 200)
)
# chart1$show()
chart1$save("pdf/page6_chart1_bank_capital1_1.pdf")

chart2 <- Chart(
  df_r2,
  indexcol='dates',
  linecols  =  c("Capital", "Core capital"),
  rlinecols = "Risk weighted Assets (RHS)",
  attrs = attrs,
  title      = "Bank Capital",
  subtitle   = "(Percent of risk-weighted assets; RWA y/y percent change)",
  legend_left = 0.4,
  xrange     = "2022-01:",
  yrange     = c(10, 25),
  ryrange    = c(120, 200)
)
# chart2$show()
chart2$save("pdf/page6_chart1_bank_capital1_2.pdf")


chart3 <- Chart(
  py_df,
  linecols  =  c("Capital", "Core capital"),
  rlinecols = "Risk weighted Assets (RHS)",
  attrs = attrs,
  title      = "Bank Capital",
  subtitle   = "(Percent of risk-weighted assets; RWA y/y percent change)",
  legend_left = 0.4,
  xrange     = "2022-01:",
  yrange     = c(10, 25),
  ryrange    = c(120, 200)
)
# chart3$show()
chart3$save("pdf/page6_chart1_bank_capital1_3.pdf")
