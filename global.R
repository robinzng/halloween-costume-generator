library(shiny)
library(shinydashboard)
library(readxl)
library(DT)
library(tidyverse)
library(fresh)

# Dataload ----------------------------------------------------------------

costumes <- readxl::read_xlsx(path=normalizePath(file.path('./www/',"halloween_costume_generator.xlsx")))

costumes_duped <- costumes %>%
  separate_rows(., outerwear_color, sep=", ") %>%
  separate_rows(., outerwear_style, sep=", ") %>%
  separate_rows(., top_color, sep=", ") %>%
  separate_rows(., top_style, sep=", ") %>%
  separate_rows(., bottom_color, sep=", ") %>%
  separate_rows(., bottom_style, sep=", ") %>%
  separate_rows(., one_piece_color, sep=", ") %>%
  separate_rows(., one_piece_style, sep=", ") %>%
  separate_rows(., shoe_color, sep=", ") %>%
  separate_rows(., shoe_style, sep=", ")
  

# Global variables --------------------------------------------------------
colors = function(piece) {
  column = paste(piece, '_color', sep='')
  
  colors <- costumes %>%
    select(all_of(column)) %>%
    separate_rows(all_of(column), sep=", ") %>%
    unique() %>%
    na.omit() %>%
    as.vector() 
  
  return(sort(colors[[1]]))
  
}


styles = function(piece) {
  column = paste(piece, '_style', sep='')
  
  styles <- costumes %>%
    select(all_of(column)) %>%
    separate_rows(all_of(column), sep=", ") %>%
    unique() %>%
    na.omit() %>%
    as.vector()
  
  return(sort(styles[[1]]))
  
}