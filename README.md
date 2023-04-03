# ODKCleaner

ODKCleaner is a web app that generates Stata cleaning code for your ODK-generated dataset. Simply upload your XLSForm and get the cleaning code ready for your data.

## Features

-   Generate Stata variable labels based on your XLSForm
-   Generate value labels for single choice variables
-   Handle select_multiple questions, either by splitting them into binary variables or labeling them if they are already split
-   Remove note variables from the dataset
-   Support for different languages in the questionnaire

## Getting Started

To use ODKCleaner, simply follow these steps:

1.  Open the web app at [ODKCleaner](https://odk-stata.streamlit.app/)
2.  Upload your XLSForm (the questionnaire in .xlsx format) from your Kobo/ODK Cloud/SurveyCTO dashboard
3.  Choose the questionnaire labels to use as your variable labels
4.  Specify how you want to handle select_multiple questions
5.  Get the generated Stata cleaning code
 
## Dependencies

-   streamlit
-   pandas
-   openpyxl

----------

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository on GitHub
2.  Create a new branch for your changes
3.  Make your changes and commit them to your branch
4.  Create a pull request to merge your changes into the main repository
5.  Wait for your pull request to be reviewed and merged