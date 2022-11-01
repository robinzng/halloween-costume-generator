ui <- fluidPage(
  use_googlefont("Work Sans"), 
  
  tags$head(
    tags$link(rel='stylesheet', type='text/css', href='styles.css')
  ),
  
  # Application title
  titlePanel("Halloween Costume Generator"),
  
  fluidRow(
    column(2, wellPanel(selectInput('outerwear_colors', "Outerwear Colors", 
                                    choices = colors('outerwear'), multiple = TRUE),
                        selectInput('outerwear_styles', "Outerwear Styles",
                                    choices = styles('outerwear'), multiple = TRUE))),
    column(2, wellPanel(selectInput('tops_colors', "Top Colors", 
                                    choices = colors('top'), multiple = TRUE),
                        selectInput('tops_styles', "Top Styles", 
                                    choices = styles('top'), multiple = TRUE))),
    column(2, wellPanel(selectInput('bottoms_colors', "Bottom Colors", 
                                    choices = colors('bottom'), multiple = TRUE),
                        selectInput('bottoms_styles', "Bottom Styles",
                                    choices = styles('bottom'), multiple = TRUE))),
    column(2, wellPanel(selectInput('one_piece_colors', "Dress/Jumpsuit Colors", 
                                    choices = colors('one_piece'), multiple = TRUE),
                        selectInput('one_piece_styles', "Dress/Jumpsuit Styles",
                                    choices = styles('one_piece'), multiple = TRUE))),
    column(2, wellPanel(selectInput('shoes_colors', "Shoe Colors",
                                    choices = colors('shoe'), multiple = TRUE),
                        selectInput('shoes_styles', "Shoe Styles",
                                    choices = styles('shoe'), multiple = TRUE))),
    column(2, actionButton('go', 'Go!'))),
  
  mainPanel(
    fluidRow(
      dataTableOutput('options')
      ),
    fluidRow(
      uiOutput('test')
    )
  )

)

