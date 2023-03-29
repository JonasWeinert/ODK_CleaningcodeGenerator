# ODKCleaner

ODKCleaner is a web application that produces STATA cleaning code for your ODK-generated dataset. It allows users to upload their XLSForm files and generates cleaning code for STATA.

## Features

- Creates Variable labels
- Creates value label based on list_names  
- Reformats date and time variables from strings
-   Optionally splits `select_multiple` fields in Stata instead of at export

## Usage

To use ODKCleaner, simply upload your XLSForm file to the web application. You can find the XLSForm of your questionnaire in your dashboard on Kobo/ODK Cloud/SurveyCTO. Click [here](https://xlsform.org/en/) for more information. Make sure that your xlsx file contains a `survey` and a `choices` sheet.
Once you have uploaded your XLSForm file, the application will ask you to choose the set of questionnaire labels that you want to use as your variable labels. You will also be asked to specify a separator symbol for `select_multiple` fields, if your form contains any.

After providing this information, the application will generate the cleaning code for STATA. The code can be copied and pasted into your STATA environment.


Once the cleaning code has been generated, the user can copy and paste it into their STATA environment.

## Author

This web application was developed by Jonas Weinert.

## Support

If you need more specialized help with your ODK or Stata projects, please contact me

-   [LinkedIn](https://www.linkedin.com/in/jweinert1997/)
-  [Email: jonas.weinert@gmail.com](mailto:jonas.weinert@gmail.com)

## Contributing

To contribute to this project, please visit the [ODKCleaner GitHub repository](https://github.com/JonasWeinert/ODK_CleaningcodeGenerator/).

## License

This project is licensed under the MIT License - see the [LICENSE](https://chat.openai.com/LICENSE) file for details.
Please give this repository a star if you use some of the code in it.